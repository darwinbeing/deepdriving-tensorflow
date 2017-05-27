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
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle, Color

import numpy as np

class DriveImage(Widget):
  _Texture = None
  _Memory = None

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._initTexture()
    MyApp = App.get_running_app()
    MyApp.registerUpdateFunc(self, self.updateTexture)

  def __del__(self):
    self._Memory = None
    self._Texture = None

  def _updateRect(self, Instance, Value):
    self._Rectangle.pos = Instance.pos
    self._Rectangle.size = Instance.size


  def _initTexture(self):
    if self._Memory != None:
      Width = self._Memory.ImageWidth
      Height = self._Memory.ImageHeight
      self._Texture = kivy.graphics.texture.Texture.create(size=(Width, Height), colorfmt='rgb')
      self._Texture.add_reload_observer(self._populateTexture)
      self._populateTexture()

      with self.canvas:
        self._Rectangle = Rectangle(texture=self._Texture, pos=self.pos, size=self.size)
        self.bind(size=self._updateRect, pos=self._updateRect)

  def updateTexture(self, *args):
    if self._Texture == None:
      self._initTexture()

    self._populateTexture()
    self.canvas.ask_update()


  def _populateTexture(self):
    if (self._Memory != None) and (self._Texture != None):
      self._Texture.blit_buffer(np.flip(self._Memory.RawImage, 2).tostring(), bufferfmt="ubyte", colorfmt="rgb")

