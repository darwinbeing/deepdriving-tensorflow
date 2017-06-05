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

from kivydd.widgets import _BACKGROUND_COLOR
from kivy.config import Config
Config.set('graphics','resizable',1)

from kivy.core.window import Window
Window.size       = (645, 700)
Window.clearcolor = _BACKGROUND_COLOR

from deep_driving.gui import CTranslateWindow, CTranslateMainApp

import dd.data_reader as dddr

import time

class CApplication(CTranslateMainApp):
  App = None
  _TranslateFrom = 0
  _TranslateTo   = 0
  _LastUpdate = time.clock()

  def initMemory(self):
    return None

  def initApp(self, Memory, App):
    self.App = App

  _LastRaceID = -1
  def doLoop(self, Memory, App):
    if self.IsTranslating:
      self._doTranslate(self.InputCursor)

    else:
      time.sleep(0.01)

    return True

  def _doTranslate(self, Cursor):
    if Cursor != None:
      self.translateSingle(Cursor)
      self._waitForUpdate()

      if not self.InputCursor.next():
        self.stopTranslating()

      else:
        if time.clock() - self._LastUpdate > 1.0:
          self.App.update()
          self._LastUpdate = time.clock()

        if self.InputCursor.Key >= self._TranslateTo:
          self.stopTranslating()

    else:
      self.stopTranslating()


  def translateSingle(self, Cursor):
    pass


  def _waitForUpdate(self):
    while (self.App.IsUpdating == True) and (self._IsExit == False):
      time.sleep(0.001)


  def openLevelDBDatabase(self, DatabasePath):
    if self.IsTranslating:
      return

    if self.InputCursor != None:
      self.InputCursor = None

    self.InputDB = None

    if DatabasePath != "":
      self.InputDB = dddr.CDataReader(DatabasePath)
      self.InputCursor = self.InputDB.getCursor()
      self.App.update()


  def stopTranslating(self):
    self.IsTranslating = False
    self.App.update()
    self._waitForUpdate()


  def startTranslating(self, From, To):
    self._TranslateFrom = From
    self._TranslateTo   = To
    self._LastUpdate = time.clock()

    if (self.InputCursor != None) and (self.InputDB != None):
      if not self.InputCursor.setKey(self._TranslateFrom):
        print("Error: Cannot translate from {} to {}, since key {} is invalid!".format(From, To, From))

      self.IsTranslating = True
      self.App.update()


  def __del__(self):
    self.InputCursor = None
    self.InputDB = None
    self.App = None


if __name__ == '__main__':
  CApplication("translate").run(CTranslateWindow)