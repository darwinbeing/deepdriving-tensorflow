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
import debug

from .. import struct
from .. import initializer
from .. import Setup
from ... import helpers

class CPooling(struct.CNamedLayer):
  def __init__(self, Window, Stride, Type = "MAX", Padding = "SAME", Name = "Pooling"):
    super().__init__(Name)
    self._Window  = Window
    self._Stride  = Stride
    self._Type    = Type
    self._Padding = Padding

  def copy(self):
    New = CPooling(Window=self._Window, Stride=self._Stride)
    New = self._copyArgs(New)
    return New

  def _copyArgs(self, New):
    New = super()._copyArgs(New)
    New._Window      = self._Window
    New._Stride      = self._Stride
    New._Type        = self._Type
    New._Padding     = self._Padding
    return New

  def __call__(self, Window = args.NotSet, Stride = args.NotSet, Type = args.NotSet, Padding = args.NotSet, Name = args.NotSet):
    New = super().__call__(Name)

    if args.isSet(Window):
      New._Window = Window

    if args.isSet(Stride):
      New._Stride = Stride

    if args.isSet(Padding):
      New._Padding = Padding

    if args.isSet(Type):
      New._Type = Type

    return New

  def setWindow(self, Window):
    self._Window = Window
    return self

  def setStride(self, Stride):
    self._Stride = Stride
    return self

  def setType(self, Type):
    self._Type = Type
    return self

  def setPadding(self, Padding):
    self._Padding = Padding
    return self

  def _apply(self, Input):
    Temp = self.copy()

    debug.Assert(Temp._Window  != None, "You have to specify the window of this pooling layer.")
    debug.Assert(Temp._Stride  != None, "You have to specify the stride of this pooling layer.")

    if Temp._Type in ["max", "MAX"]:
      Func = tf.nn.max_pool
    elif Temp._Type in ["avg", "AVG"]:
      Func = tf.nn.avg_pool
    else:
      debug.logError("Unknown pooling function: {}".format(Temp._Type))

    Setup.log("* Pooling-Type: {}".format(Temp._Type))

    if isinstance(Temp._Window, int):
      WindowShape = [1, int(Temp._Window), int(Temp._Window), 1]
    else:
      WindowShape = [1, int(Temp._Window[0]), int(Temp._Window[1]), 1]

    Setup.log("* Pooling-Window: {}".format(WindowShape[1], WindowShape[2]))

    if isinstance(Temp._Stride, int):
      StrideShape = [1, int(Temp._Stride), int(Temp._Stride), 1]
    else:
      StrideShape = [1, int(Temp._Stride[0]), int(Temp._Stride[1]), 1]

    Setup.log("* Stride: {}".format(StrideShape[1], StrideShape[2]))

    Input = Func(Input, ksize=WindowShape, strides=StrideShape, padding=Temp._Padding)

    Setup.log("* Output-Shape: {}".format(Input.shape))

    return Input