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
# Note: The DeepDriving project on pithis repository is derived from the DeepDriving project devloped by the princeton
# university (http://deepdriving.cs.princeton.edu/). The above license only applies to the parts of the code, which 
# were not a derivative of the original DeepDriving project. For the derived parts, the original license and 
# copyright is still valid. Keep this in mind, when using code from this project.

from kivydd.widgets import _BACKGROUND_COLOR
from kivy.config import Config
Config.set('graphics','resizable',1)
from kivy.core.window import Window
Window.size       = (645, 700)
Window.clearcolor = _BACKGROUND_COLOR

import speed_dreams as sd
import dd.drive_controller as dddc
import dd
from kivydd.app import CAppThread, Widget

import deep_driving.model as model
import deep_learning as dl
import misc

class DriveWindow(Widget):
  LayoutFile = "drive.kv"

class CInferenceSettings(misc.settings.CSettings):
  _Dict = {
  'Data': {
    'ImageWidth': 280,
    'ImageHeight': 210
  },
  'Inference': {
    'CheckpointPath':   'Checkpoint',
    'Epoch': None,
  },
  'PreProcessing':
  {
    'MeanFile': 'image-mean.tfrecord'
  },
  }

SettingFile = "inference.cfg"

class CApplication(CAppThread):

  _Model     = None
  _Settings  = None
  _Inference = None
  def initMemory(self):
    self._Settings  = CInferenceSettings(SettingFile)
    self._Model     = dl.CModel(model.CAlexNet)
    self._Inference = self._Model.createInference(model.CInference, model.CInferenceReader, self._Settings)
    self._Inference.restore()

    Memory = sd.CSharedMemory()
    Memory.setSyncMode(True)
    return Memory

  _IsAIEnabled = True
  def enableAI(self):
    self._IsAIEnabled = True

  def disableAI(self):
    self._IsAIEnabled = False

  _IsDriverEnabled = False
  def enableDriver(self):
    self._IsDriverEnabled = True

  def disableDriver(self):
    self._IsDriverEnabled = False

  _Labels = dd.Indicators_t()
  def initApp(self, Memory, App):
    App.setLabels(self._Labels)

  _LastRaceID = 0
  def doLoop(self, Memory, App):
    if Memory.read():
      if Memory.Data.Game.UniqueRaceID != self._LastRaceID:
        self._initRace(Memory)
      self.control(Memory, App)
      Memory.indicateReady()
      App.update()

    else:
      import time
      time.sleep(0.001)

    return True


  _DriveController = None
  _Indicators      = None
  _Control         = None
  def _initRace(self, Memory):
    print("Initialize a new race...")
    self._DriveController = dddc.CDriveController(Memory.Data.Game.Lanes)
    self._Indicators      = dd.Indicators_t()
    self._Control         = dd.Control_t()
    self._LastRaceID      = Memory.Data.Game.UniqueRaceID


  _PerformanceOutput = 100
  _CurrentRun = 0
  def control(self, Memory, App):
    if self._IsAIEnabled:
      Image = Memory.Image
      self._Indicators = self._Inference.run([Image])
      self._Indicators.Speed  = Memory.Data.Game.Speed
      self._Indicators.copyTo(self._Labels)
      App._DrawLabels = True

      self._CurrentRun += 1
      if self._CurrentRun > self._PerformanceOutput:
        print("Run-Time: {:.3f}s; Mean-Time: {:.3f}s".format(self._Inference.getLastTime(), self._Inference.getMeanTime()))
        self._CurrentRun = 0


    else:
      self._Indicators.Speed  = Memory.Data.Game.Speed
      self._Indicators.Fast   = Memory.Data.Labels.Fast
      self._Indicators.Angle  = Memory.Data.Labels.Angle
      self._Indicators.LL     = Memory.Data.Labels.LL
      self._Indicators.ML     = Memory.Data.Labels.ML
      self._Indicators.MR     = Memory.Data.Labels.MR
      self._Indicators.RR     = Memory.Data.Labels.RR
      self._Indicators.DistLL = Memory.Data.Labels.DistLL
      self._Indicators.DistMM = Memory.Data.Labels.DistMM
      self._Indicators.DistRR = Memory.Data.Labels.DistRR
      self._Indicators.L      = Memory.Data.Labels.L
      self._Indicators.M      = Memory.Data.Labels.M
      self._Indicators.R      = Memory.Data.Labels.R
      self._Indicators.DistL  = Memory.Data.Labels.DistL
      self._Indicators.DistR  = Memory.Data.Labels.DistR
      self._Labels.reset()
      App._DrawLabels = False

    self._DriveController.control(self._Indicators, self._Control)

    Memory.Data.Control.IsControlling = self._IsDriverEnabled
    Memory.Data.Control.Steering      = self._Control.Steering
    Memory.Data.Control.Accelerating  = self._Control.Accelerating
    Memory.Data.Control.Breaking      = self._Control.Breaking

if __name__ == '__main__':
  CApplication("drive").run(DriveWindow)