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

import debug
import tensorflow as tf
import misc.arguments as args

from .. import Setup
from .. import struct

class CDropout(struct.CNamedLayer):
  def __init__(self, KeepRatio = 0.5, Name = "Dropout"):
    super().__init__(Name, DoPrint=False)
    self._KeepRatio = KeepRatio

  def copy(self):
    New = CDropout()
    New = self._copyArgs(New)
    return New


  def _copyArgs(self, New):
    New = super()._copyArgs(New)
    New._KeepRatio = self._KeepRatio
    return New


  def __call__(self, KeepRatio = args.NotSet, Name = args.NotSet):
    New = super().__call__(Name)

    if args.isSet(KeepRatio):
      New._KeepRatio = KeepRatio

    return New

  def _apply(self, Input):
    Temp = self.copy()

    Setup.log("* Dropout with keep ratio {}".format(Temp._KeepRatio))
    debug.Assert(Setup.IsTraining is not None, "You must define the IsTraining boolean before using Dropout!")
    return tf.layers.dropout(Input, rate=Temp._KeepRatio, training=Setup.IsTraining)
