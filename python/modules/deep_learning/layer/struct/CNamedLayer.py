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
import misc.arguments as args

from .CLayer import CLayer
from .. import Setup

class CNamedLayer(CLayer):

  _Name = None
  def __init__(self, Name = None):
    self._Name = Name


  def copy(self):
    New = CNamedLayer()
    New = self._copyArgs(New)
    return New

  def _copyArgs(self, New):
    New._Name = self._Name
    return New

  def __call__(self, Name = args.NotSet):
    New = self.copy()

    if args.isSet(Name):
      New._Name = Name

    return New


  def apply(self, Input):
    if self._Name is not None:
      Setup.log("* Apply layer \"{}\"".format(self._Name))
      Setup.increaseLoggerIndent(2)
      with tf.name_scope(self._Name):
        Input = self._apply(Input)
      Setup.decreaseLoggerIndent(2)

    else:
      Input = self._apply(Input)

    return Input


  def _apply(self, Input):
    raise Exception("This method must be overwritten!")
    return Input