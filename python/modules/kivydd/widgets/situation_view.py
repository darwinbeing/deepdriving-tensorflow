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
import dd.situation_view as ddsv
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle, Color

import numpy as np

_BACKGROUND_COLOR = (ddsv._BACKGROUND_COLOR[0], ddsv._BACKGROUND_COLOR[1], ddsv._BACKGROUND_COLOR[2], 1.0)

class SituationView(Widget):
  _Texture             = None
  _Memory              = None
  _GroundTruth         = None
  _DrawReal            = False
  _Labels              = None
  _DrawEstimated       = False
  _SituationView       = None

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._SituationView = ddsv.CSituationView()
    self._initTexture()
    MyApp = App.get_running_app()
    MyApp.registerUpdateFunc(self, self.updateTexture)

  def __del__(self):
    self._Memory = None
    self._Texture = None
    self._Labels = None
    self._SituationView = None

  def _updateRect(self, Instance, Value):
    self._Rectangle.pos = Instance.pos
    self._Rectangle.size = Instance.size


  def _initTexture(self):
    Width = self._SituationView.getImage().shape[1]
    Height = self._SituationView.getImage().shape[0]
    self._Texture = kivy.graphics.texture.Texture.create(size=(Width, Height), colorfmt='rgb')
    self._Texture.add_reload_observer(self._populateTexture)
    self.updateTexture()

    with self.canvas:
      Color((1, 1, 1, 1))
      self._Rectangle = Rectangle(texture=self._Texture, pos=self.pos, size=self.size)
      self.bind(size=self._updateRect, pos=self._updateRect)


  def updateTexture(self, *args):
    if self._Texture == None:
      self._initTexture()

    IsRealUpdate = False
    IsEstimatedUpdate = False

    if self._DrawReal:
      if self._Memory != None:
        self._SituationView.Real.Speed  = self._Memory.Data.Game.Speed
        self._SituationView.Real.Fast   = self._Memory.Data.Labels.Fast
        self._SituationView.Real.Angle  = self._Memory.Data.Labels.Angle
        self._SituationView.Real.LL     = self._Memory.Data.Labels.LL
        self._SituationView.Real.ML     = self._Memory.Data.Labels.ML
        self._SituationView.Real.MR     = self._Memory.Data.Labels.MR
        self._SituationView.Real.RR     = self._Memory.Data.Labels.RR
        self._SituationView.Real.DistLL = self._Memory.Data.Labels.DistLL
        self._SituationView.Real.DistMM = self._Memory.Data.Labels.DistMM
        self._SituationView.Real.DistRR = self._Memory.Data.Labels.DistRR
        self._SituationView.Real.L      = self._Memory.Data.Labels.L
        self._SituationView.Real.M      = self._Memory.Data.Labels.M
        self._SituationView.Real.R      = self._Memory.Data.Labels.R
        self._SituationView.Real.DistL  = self._Memory.Data.Labels.DistL
        self._SituationView.Real.DistR  = self._Memory.Data.Labels.DistR
        IsRealUpdate = True

      elif self._GroundTruth != None:
        self._SituationView.Real.Speed  = self._GroundTruth.Speed
        self._SituationView.Real.Fast   = self._GroundTruth.Fast
        self._SituationView.Real.Angle  = self._GroundTruth.Angle
        self._SituationView.Real.LL     = self._GroundTruth.LL
        self._SituationView.Real.ML     = self._GroundTruth.ML
        self._SituationView.Real.MR     = self._GroundTruth.MR
        self._SituationView.Real.RR     = self._GroundTruth.RR
        self._SituationView.Real.DistLL = self._GroundTruth.DistLL
        self._SituationView.Real.DistMM = self._GroundTruth.DistMM
        self._SituationView.Real.DistRR = self._GroundTruth.DistRR
        self._SituationView.Real.L      = self._GroundTruth.L
        self._SituationView.Real.M      = self._GroundTruth.M
        self._SituationView.Real.R      = self._GroundTruth.R
        self._SituationView.Real.DistL  = self._GroundTruth.DistL
        self._SituationView.Real.DistR  = self._GroundTruth.DistR
        IsRealUpdate = True

    if (self._Labels != None) and self._DrawEstimated:
      self._SituationView.Estimated.Speed  = 0
      self._SituationView.Estimated.Fast   = self._Labels.Fast
      self._SituationView.Estimated.Angle  = self._Labels.Angle
      self._SituationView.Estimated.LL     = self._Labels.LL
      self._SituationView.Estimated.ML     = self._Labels.ML
      self._SituationView.Estimated.MR     = self._Labels.MR
      self._SituationView.Estimated.RR     = self._Labels.RR
      self._SituationView.Estimated.DistLL = self._Labels.DistLL
      self._SituationView.Estimated.DistMM = self._Labels.DistMM
      self._SituationView.Estimated.DistRR = self._Labels.DistRR
      self._SituationView.Estimated.L      = self._Labels.L
      self._SituationView.Estimated.M      = self._Labels.M
      self._SituationView.Estimated.R      = self._Labels.R
      self._SituationView.Estimated.DistL  = self._Labels.DistL
      self._SituationView.Estimated.DistR  = self._Labels.DistR
      IsEstimatedUpdate = True

    self._SituationView.update(IsRealUpdate, IsEstimatedUpdate)
    self._populateTexture()
    self.canvas.ask_update()

  def _populateTexture(self):
    if (self._Texture != None) and (self._SituationView != None):
      Image = self._SituationView.getImage()
      Image = np.flip(Image, 2)
      Image = np.flip(Image, 0)
      self._Texture.blit_buffer(Image.tostring(), bufferfmt="ubyte", colorfmt="rgb")

  def setGroundTruth(self, Indicators):
    self._GroundTruth = Indicators
    self.updateTexture()