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

import tensorflow as tf
import time
import debug

from .. import internal
from .. import data
from .. import helpers

class CMeanCalculator(internal.CBaseRunner):
  def __init__(self, ReaderFactoryArg, Settings):
    super().__init__(Settings)
    ReaderFactory    = internal.getFactory(ReaderFactoryArg, data.CFactory, data.CReader)
    self._Reader = ReaderFactory.create(Settings, IsTraining=True, IsPreprocessing=False)
    self._Targets = self._buildTarget(self._Reader)
    self._MeanImageList = []
    self._VarImageList  = []
    self._MeanColorList = []
    self._VarColorList  = []
    self._MeanImage     = None
    self._VarImage      = None
    self._MeanColor     = None
    self._VarColor      = None
    self._MeanReader    = data.CMeanReader()

  def calculate(self):
    self._MeanImageList = []
    self._VarImageList  = []
    self._MeanColorList = []
    self._VarColorList  = []
    self._MeanImage     = None
    self._VarImage      = None
    self._MeanColor     = None
    self._VarColor      = None

    Session = self._Session

    # Start queues
    QueueCoordinage = tf.train.Coordinator()
    tf.train.start_queue_runners(sess=Session, coord=QueueCoordinage)

    # Calculate number of epochs to run
    MaxEpochs = self.getMaxEpochs()

    # Loop Preparation
    BatchSize = self._Reader.getBatchSize()
    Epoch = 0
    IterationsPerEpoch = helpers.getIterationsPerEpoch(self.getEpochSize(), BatchSize)
    Iteration = Epoch * IterationsPerEpoch
    print("Run mean-calculation for {} epochs beginning with epoch {} and {} iterations per epoch.".format(MaxEpochs, 0, IterationsPerEpoch))

    # Evaluation Loop
    StartTime = time.time()
    for EpochNumber in range(MaxEpochs):
      Epoch = EpochNumber + 1
      SampleCount = 0
      for Batch in range(IterationsPerEpoch):
        Iteration += 1
        SampleCount += BatchSize
        self._printProgressBar("Calculation", 20, Iteration, Epoch, Batch, IterationsPerEpoch)
        Results = self._internalCalculationStep(Session, Iteration, Batch, Epoch)
        self._addResults(Results)

      StartTime = self._postEpochAction(Results, StartTime, Iteration, Epoch, SampleCount)

    # Stop queues
    QueueCoordinage.request_stop()
    QueueCoordinage.join()

    MergedResults = self._mergeResults()


  def _internalCalculationStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = self._Targets
    #+ [tf.reshape(self._Reader.getOutputs()['Image'], shape=[32, 32, 3])]
    Results = list(self._calculationIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))
    return Results


  def _postEpochAction(self, Results, StartTime, Iteration, Epoch, SampleCount):
    Duration = (time.time() - StartTime)
    StartTime = time.time()

    ProgressString = "{}: ".format(str(Iteration).rjust(8))
    ProgressString += "[MeanCalc] "
    ProgressString += "Progress Epoch {}".format(str(Epoch).rjust(3))
    ProgressString += "/{}".format(str(self.getMaxEpochs()).rjust(3))
    ProgressString += " ("
    ProgressString += "{:.3f} s/Epoch".format(Duration)
    ProgressString += ", "

    if Duration > 0:
      SamplesPerSec = SampleCount/Duration
    else:
      SamplesPerSec = 0

    ProgressString += "{:.3f} Samples/s".format(SamplesPerSec)
    ProgressString += ")"
    print(ProgressString)

    return StartTime


  def _addResults(self, Results):
    self._MeanImageList.append(Results[0])
    self._VarImageList.append(Results[1])
    self._MeanColorList.append(Results[2])
    self._VarColorList.append(Results[3])


  def _mergeResults(self):
    N = len(self._MeanImageList)

    debug.Assert(N == len(self._VarImageList))
    debug.Assert(N == len(self._MeanColorList))
    debug.Assert(N == len(self._VarColorList))

    if N > 0:
      self._MeanImage = self._mergeMean(self._MeanImageList, N)
      self._VarImage  = self._mergeVar(self._VarImageList, self._MeanImageList, N)
      self._MeanColor = self._mergeMean(self._VarColorList, N)
      self._VarColor  = self._mergeVar(self._VarColorList, self._MeanColorList, N)


  def _mergeMean(self, List, N):
    Sum = None
    for Element in List:
      if Sum is None:
        Sum = Element
      else:
        Sum += Element

    return Sum/N


  def _mergeVar(self, VarList, MeanList, N):
    VarSum  = None
    MeanSum = None

    for i in range(N):
      #print("Element {} with Var {} and Mean {}".format(i, VarList[i], MeanList[i]))
      VarElement  = VarList[i] + MeanList[i] * MeanList[i]
      MeanElement = MeanList[i]

      if VarSum is None or MeanSum is None:
        VarSum  = VarElement
        MeanSum = MeanElement

      else:
        VarSum  += VarElement
        MeanSum += MeanElement


    Mean = MeanSum/N
    Var  = VarSum/N - Mean*Mean

    #print("Merged Var {} and Mean {}".format(Var, Mean))

    return Var


  def store(self):
    debug.Assert(self._MeanImage is not None, "You must calculate the mean and var values before store the resuls!")
    debug.Assert(self._VarImage  is not None, "You must calculate the mean and var values before store the resuls!")
    debug.Assert(self._MeanColor is not None, "You must calculate the mean and var values before store the resuls!")
    debug.Assert(self._VarColor  is not None, "You must calculate the mean and var values before store the resuls!")
    self._MeanReader.store(self._Settings['MeanCalculator']['MeanFile'], self._MeanImage, self._VarImage, self._MeanColor, self._VarColor)


  def getMaxEpochs(self):
    return self._getMaxEpochs(self._Settings)



  def getEpochSize(self):
    return self._getEpochSize(self._Settings)


  def _getMaxEpochs(self, Settings):
    # You have to overwride this method to return the maximum number of epochs.
    return Settings['MeanCalculator']['NumberOfEpochs']


  def _getEpochSize(self, Settings):
    # You have to overwride this method to return the epoch size.
    return Settings['MeanCalculator']['EpochSize']


  def _buildTarget(self, Reader):
    Image = self._getImage(Reader)

    MeanImage, VarianceImage = tf.nn.moments(Image, axes=[0])
    MeanColor, VarianceColor = tf.nn.moments(Image, axes=[0, 1, 2])

    return [MeanImage, VarianceImage, MeanColor, VarianceColor]


  def _getImage(self, Reader):
    # You must overwrite this method in your own class.
    raise Exception("This method must be overwritten and return an image tensor.")


  def _calculationIteration(self, Session, RunTargets, Reader, Iteration, Batch, Epoch):
    # You must overwrite this method in your own class.
    raise Exception("This method must be overwritten and return the target-results.")
