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

from kivy.uix.popup import Popup
import kivygarden as garden
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import App
from kivy.uix.widget import Widget

import os
import misc.settings

import dd
from kivydd.app import CAppThread

from ..legacy import translateLabels

_CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

class CTranlateSettings(misc.settings.CSettings):
  _Dict = {
    'LastLevelDBPath': os.getcwd(),
    'LastOutputPath': os.getcwd(),
    'FromKey': 0,
    'ToKey': 0,
    'RaceID': -1,
    'TrackName': "Unknown"
  }

class CTranslateMainApp(CAppThread):
  InputDB       = None
  InputCursor   = None
  IsTranslating = False

  def startTranslating(self, From, To, TrackName, TrackID, RaceID):
    raise Exception("This method must be overwritten...")

  def openLevelDBDatabase(self, DatabasePath):
    raise Exception("This method must be overwritten...")

  def setTFRecordDatabase(self, DatabasePath):
    raise Exception("This method must be overwritten...")



class CTranslateWindow(Widget):
  LayoutFile = os.path.join(_CURRENT_SCRIPT_PATH, "translate.kv")
  _PopUp = None
  _Settings = CTranlateSettings("translate.cfg")
  _LevelDBPath = StringProperty("")
  _OutputPath = StringProperty(_Settings['LastOutputPath'])
  _GroundTruth = dd.Indicators_t()
  _DisableAll = BooleanProperty(False)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    if self._isLevelDBDatabase(self._Settings['LastLevelDBPath']):
      self._LevelDBPath = self._Settings['LastLevelDBPath']
    else:
      self._LevelDBPath = ""

    MyApp = App.get_running_app()
    MyApp.registerUpdateFunc(self, self.updateCursor)

    if not isinstance(MyApp._Main, CTranslateMainApp):
      raise Exception("The main up must be inherited from CTranslateMainApp")

    MyApp._Main.openLevelDBDatabase(self._LevelDBPath)
    MyApp._Main.setTFRecordDatabase(self._OutputPath)

    self.ids.FromTextInput.text      = str(self._Settings['FromKey'])
    self.ids.ToTextInput.text        = str(self._Settings['ToKey'])
    self.ids.RaceIDTextInput.text    = str(self._Settings['RaceID'])
    self.ids.TrackNameTextInput.text = str(self._Settings['TrackName'])

  def _closePopup(self):
    if self._PopUp != None:
      self._PopUp.dismiss()

  def _showPopup(self, Title, Content):
    self._PopUp = Popup(title=Title, content=Content, size_hint=(0.95, 0.95))
    self._PopUp.open()


  def selectInputPath(self, *args):
    Content = garden.file_browser.FileBrowser(select_string="Open Folder", favorites=[(self._Settings['LastLevelDBPath'], 'Last Path')])
    Content.bind(on_success=self._openDir, on_canceled=self._cancelOpenDir)
    Content.dirselect = True
    Content.path = self._Settings['LastLevelDBPath']
    if not os.path.exists(Content.path):
      Content.path = os.getcwd()
    self._showPopup(Title="Open LevelDB Directory...", Content=Content)


  def selectOutputPath(self, *args):
    LastPath = self._Settings['LastOutputPath']
    LastFile = ""
    while not os.path.exists(LastPath):
      LastFile = os.path.basename(LastPath)
      NewPath = os.path.dirname(LastPath)
      if NewPath == LastPath:
        LastPath = os.getcwd()
        break
      LastPath = NewPath
    Content = garden.file_browser.FileBrowser(select_string="Select Folder", favorites=[(LastPath, 'Last Path')])
    Content.bind(on_success=self._selectDir, on_canceled=self._cancelOpenDir)
    Content.dirselect = True
    Content.path = LastPath
    if not os.path.exists(Content.path):
      Content.path = os.getcwd()
    self._showPopup(Title="Select Output Directory...", Content=Content)
    Content.filename = LastFile


  def _openDir(self, Instance):
    if len(Instance.selection) > 0:
      self._Settings['LastLevelDBPath'] = Instance.selection[0]
    else:
      self._Settings['LastLevelDBPath'] = Instance.path
    self._closePopup()
    self._Settings.store()
    if self._isLevelDBDatabase(self._Settings['LastLevelDBPath']):
      self._LevelDBPath = self._Settings['LastLevelDBPath']
    else:
      self._LevelDBPath = ""

    MyApp = App.get_running_app()
    MyApp._Main.openLevelDBDatabase(self._LevelDBPath)

  def _selectDir(self, Instance):
    if len(Instance.selection) > 0:
      if Instance.filename != "":
        self._Settings['LastOutputPath'] = Instance.filename
      else:
        self._Settings['LastOutputPath'] = Instance.selection[0]
    else:
      if Instance.filename != "":
        self._Settings['LastOutputPath'] = os.path.join(Instance.path, Instance.filename)
      else:
        self._Settings['LastOutputPath'] = Instance.path
    self._closePopup()
    self._Settings.store()
    self._OutputPath = self._Settings['LastOutputPath']

    MyApp = App.get_running_app()
    MyApp._Main.setTFRecordDatabase(self._OutputPath)


  def _cancelOpenDir(self, Instance):
    self._closePopup()


  def _isLevelDBDatabase(self, DatabasePath):
    CurrentFilename = os.path.join(DatabasePath, "CURRENT")
    return os.path.exists(CurrentFilename)


  def enterTrackName(self, Instance, Value):
    if Instance.focus or Value == self._Settings['TrackName']:
      return

    self._Settings['TrackName'] = Value
    self._Settings.store()


  def enterRaceID(self, Instance, Value):
    Value = int(Value)
    if Instance.focus or Value == self._Settings['RaceID']:
      return

    self._Settings['RaceID'] = Value
    self._Settings.store()


  def enterFrameNumber(self, Instance, Value):
    Value = int(Value)
    if Instance.focus:
      return

    MyApp   = App.get_running_app()
    Cursor  = MyApp._Main.InputCursor
    InputDB = MyApp._Main.InputDB

    if (Cursor != None) and (InputDB != None):
      CurrentKey = Cursor.Key
      if Value >= InputDB.FirstKey and Value <= InputDB.LastKey:
        if not Cursor.setKey(int(Value)):
          print("Key {} does not exist, switch back to old key {}.".format(Value, CurrentKey))
          Cursor.setKey(CurrentKey)
          self.ids.FrameTextInput.text = str(CurrentKey)

        self.updateCursor()

      else:
        self.ids.FrameTextInput.text = str(CurrentKey)


  def enterFromFrame(self, Instance, Value):
    Value = int(Value)
    if Instance.focus or Value == self._Settings['FromKey']:
      return

    MyApp = App.get_running_app()
    InputDB = MyApp._Main.InputDB

    if InputDB != None:
      if Value >= InputDB.FirstKey and Value <= InputDB.LastKey:
        self._Settings['FromKey'] = Value
        self._Settings.store()

      else:
        self._Settings['FromKey'] = InputDB.FirstKey
        self.ids.FromTextInput.text = str(self._Settings['FromKey'])
        self._Settings.store()


  def enterToFrame(self, Instance, Value):
    Value = int(Value)
    if Instance.focus or Value == self._Settings['ToKey']:
      return

    MyApp = App.get_running_app()
    InputDB = MyApp._Main.InputDB

    if InputDB != None:
      if Value >= InputDB.FirstKey and Value <= InputDB.LastKey:
        self._Settings['ToKey'] = Value
        self._Settings.store()

      else:
        self._Settings['ToKey'] = InputDB.LastKey
        self.ids.ToTextInput.text = str(self._Settings['ToKey'])
        self._Settings.store()

  def move(self, Step):
    MyApp   = App.get_running_app()
    Cursor  = MyApp._Main.InputCursor
    InputDB = MyApp._Main.InputDB

    if (Cursor != None) and (InputDB != None):
      CurrentKey = Cursor.Key
      NewKey = CurrentKey + Step

      if NewKey < InputDB.FirstKey:
        NewKey = InputDB.FirstKey

      if NewKey > InputDB.LastKey:
        NewKey = InputDB.LastKey

      if not Cursor.setKey(NewKey):
        print("Key {} does not exist, switch back to old key {}.".format(NewKey, CurrentKey))
        Cursor.setKey(CurrentKey)

      self.updateCursor()

  def updateCursor(self, *args):
    MyApp = App.get_running_app()
    Cursor = MyApp._Main.InputCursor

    if int(self.ids.FromTextInput.text) < MyApp._Main.InputDB.FirstKey:
      self._Settings['FromKey'] = MyApp._Main.InputDB.FirstKey
      self.ids.FromTextInput.text = str(self._Settings['FromKey'])
      self._Settings.store()

    if int(self.ids.ToTextInput.text) < MyApp._Main.InputDB.FirstKey or int(self.ids.ToTextInput.text) > MyApp._Main.InputDB.LastKey:
      self._Settings['ToKey'] = MyApp._Main.InputDB.LastKey
      self.ids.ToTextInput.text = str(self._Settings['ToKey'])
      self._Settings.store()

    self.ids.FrameTextInput.text = str(Cursor.Key)
    self.ids.DriveImage.setImage(Cursor.Image)
    self._GroundTruth = translateLabels(self._GroundTruth, Cursor.Labels)
    self.ids.SituationView.setGroundTruth(self._GroundTruth)

    if self._DisableAll:
      CurrentKey = int(Cursor.Key)
      KeyRange = self._Settings['ToKey'] - self._Settings['FromKey']
      Percent = 0
      if KeyRange > 0:
        Percent = (CurrentKey - self._Settings['FromKey'])/(KeyRange)

      if Percent < 0:
        Percent = 0

      if Percent > 1:
        Percent = 1

      self.ids.ProgressBar.value = Percent * 100

    else:
      self.ids.ProgressBar.value = 0

    if (not MyApp._Main.IsTranslating) and self._DisableAll:
      self._DisableAll = False


  def startTranslation(self):
    MyApp   = App.get_running_app()

    import hashlib
    Hash = hashlib.md5()
    Hash.update(self._Settings['TrackName'].encode('utf-8'))

    self._DisableAll = True
    MyApp._Main.startTranslating(self._Settings['FromKey'],
                                 self._Settings['ToKey'],
                                 self._Settings['TrackName'],
                                 int(Hash.hexdigest()[0:15], 16),
                                 self._Settings['RaceID'])
