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
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty
import os

_CURRENT_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
kivy.resources.resource_add_path(_CURRENT_SCRIPT_PATH)

Builder.load_string("""
<LightButton>:
  Image:
    source: self.parent._CurrentImage
    size: (14, 14)
    y: self.parent.y + self.parent.height / 2 - self.height / 2
    x: self.parent.x + self.width / 2
""")

class LightButton(Button):
  _IsOn = False
  _CurrentImage = StringProperty("light_off.png")

  def __init__(self, **kwargs):
    self.register_event_type('on_enable')
    self.register_event_type('on_disable')
    super().__init__(**kwargs)
    self.bind(on_press=self.onPressed)
    self._updateLight(self._IsOn)
    kivy.clock.Clock.schedule_once(self._updateLight, 0)

  def onPressed(self, Instance):
    self._IsOn = not self._IsOn
    self._updateLight(self._IsOn)

  def _updateLight(self, *args):
    if self._IsOn:
      self._CurrentImage = "light_on.png"
      self.dispatch('on_enable', self._IsOn)

    else:
      self._CurrentImage = "light_off.png"
      self.dispatch('on_disable', self._IsOn)

  def on_enable(self, *args):
    pass

  def on_disable(self, *args):
    pass