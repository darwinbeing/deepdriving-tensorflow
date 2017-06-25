# The MIT license:
#
# Copyright 2017 Andre Netzeband
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#
# Note: The DeepDriving project on this repository is derived from the DeepDriving project devloped by the princeton 
# university (http://deepdriving.cs.princeton.edu/). The above license only applies to the parts of the code, which 
# were not a derivative of the original DeepDriving project. For the derived parts, the original license and 
# copyright is still valid. Keep this in mind, when using code from this project.

import debug
import os
import time

from .. import internal
from .. import checkpoint
from .. import network
from .. import data

class CInference(internal.CBaseRunner):
  def __init__(self, Network, Reader, Settings = None):
    super().__init__(Settings)
    debug.Assert(isinstance(Network, network.CNetwork), "You must specify a Network object.")
    debug.Assert(isinstance(Reader, data.CReader), "You must specify a Reader object.")

    self._Network          = Network
    self._Reader           = Reader

    self._IsReady = False
    self._prepare(self._Settings)


  def _prepare(self, Settings):
    if not self._IsReady:
      self._SampleCount = 0
      self._RunTime = 0.0
      self._MaxTime = None
      self._MinTime = None
      self._LastTime = 0.0
      self.reset(self.getCheckpointDir())
      self._IsReady = True


  def run(self, Inputs = None):
    Session = self._Session

    self._SampleCount += 1
    StartTime = time.time()

    RunTargets = []
    RawResults = list(self._runIteration(Session, RunTargets, Inputs, self._Reader, self._SampleCount))

    TimeDelta = time.time() - StartTime
    self._addTimeStatistics(TimeDelta)

    return self._postProcess(RawResults)

  # Do not store the first 10 runs, due to much overhead here
  _SampleOffset = 10
  def _addTimeStatistics(self, TimeDelta):
    if self._SampleCount > self._SampleOffset:
      self._LastTime = TimeDelta
      self._RunTime += TimeDelta

      if self._MaxTime is None:
        self._MaxTime = TimeDelta
      elif self._MaxTime < TimeDelta:
        self._MaxTime = TimeDelta

      if self._MinTime is None:
        self._MinTime = TimeDelta
      elif self._MinTime > TimeDelta:
        self._MinTime = TimeDelta


  def getLastTime(self):
    return self._LastTime


  def getMeanTime(self):
    if self._SampleCount > self._SampleOffset:
      return self._RunTime / (self._SampleCount - self._SampleOffset)
    return 0.0


  def getMaxTime(self):
    return self._MaxTime


  def getMinTime(self):
    return self._MinTime


  def _runIteration(self, Session, RunTargets, Inputs, Reader, Iteration):
    # You must overwrite this function to run a single inference step
    raise Exception("You must overwrite this function to run a single inference step.")
    return []


  def _postProcess(self, Results):
    # you can overwrite this function to post-process the result-values
    return Results


  def restore(self, Epoch=None):
    if Epoch is None:
      if "Inference" in self._Settings:
        if "Epoch" in self._Settings['Inference']:
          Epoch = self._Settings['Inference']['Epoch']

    if Epoch is None:
      CheckpointFile = checkpoint.getLatestCheckpointFile(self.getCheckpointDir())

    else:
      CheckpointFile = checkpoint.getCheckpointFilename(self.getCheckpointDir(), Epoch)

    if CheckpointFile is None:
      debug.logWarning("Cannot find any checkpoint file. Network is initialized randomly...")

    else:
      super().restore(CheckpointFile)


  def getCheckpointDir(self):
    return self._getCheckpointDir(self._Settings)

  def getUseTrace(self):
    return self._getUseTrace(self._Settings)

  def _getCheckpointDir(self, Settings):
    # You can overrite this function to specify a checkpoint directory
    if 'Inference' in Settings:
      if 'CheckpointPath' in Settings['Inference']:
        return os.path.join(Settings['Inference']['CheckpointPath'], "State_{}".format(self._Network.State))

    return None

  def _getUseTrace(self, Settings):
    # You can overrite this function to specify a checkpoint directory
    if 'Inference' in Settings:
      if 'Trace' in Settings['Inference']:
        return Settings['Inference']['Trace']

    return False

  def _getSummaryDir(self, Settings):
    return None


