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

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from .main_app import MainApp

import threading

class CAppThread():
  _Name = "main"
  _Memory = None
  _App = None
  _Thread = None
  _IsExist = False

  def __init__(self, Name):
    self._Name = Name

  def run(self, MainWindow):
    kivy.require('1.10.0')
    self._Memory = self.initMemory()
    self._App = MainApp(MainWindow, self._Memory)
    self._App.title = self._Name
    self.initApp(self._Memory, self._App)
    self._Thread = threading.Thread(target=self._mainLoop)
    self._IsExit = False
    self._Thread.start()

    self._App.run()

    self._IsExit = True
    self._Thread.join()
    self._Thread = None
    self._Memory = None
    self._App.deleteAll()
    self._App    = None

  def _mainLoop(self):
    while self._IsExit == False:
      if self.doLoop(self._Memory, self._App) == False:
        break

  def initMemory(self):
    return None

  def initApp(self, Memory, App):
    pass

  def doLoop(self, Memory, App):
    return True

