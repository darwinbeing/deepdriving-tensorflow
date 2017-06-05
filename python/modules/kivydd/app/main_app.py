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
from kivy.lang import Builder

import threading

class MainApp(App):
  _Memory = None
  _Labels = None
  _Main   = None
  IsUpdating = False

  def __init__(self, MainWindow, Memory, MainObject, **kwargs):
    super().__init__(**kwargs)
    self._UpdateTrigger = kivy.clock.Clock.create_trigger(self._update)
    self._UpdateFunctions = {}
    self._MainWindow = MainWindow
    self._Memory = Memory
    self._Window = None
    self._Main = MainObject

  def update(self):
    self.IsUpdating = True
    self._UpdateTrigger()

  def _update(self, *args):
    for Object in self._UpdateFunctions.keys():
      self._UpdateFunctions[Object]()

    self.IsUpdating = False

  def deleteAll(self):
    self._UpdateFunctions = {}
    self._Window.clear_widgets()
    self._Memory = None
    self._Labels = None
    self._Main = None

  def build(self):
    try:
      LayoutFile = self._MainWindow.LayoutFile
    except:
      LayoutFile = None

    if LayoutFile != None:
      Builder.load_file(LayoutFile)

    self._Window = self._MainWindow()
    return self._Window

  def registerUpdateFunc(self, Object, Function):
    self._UpdateFunctions[Object] = Function

  def setLabels(self, Labels):
    self._Labels = Labels