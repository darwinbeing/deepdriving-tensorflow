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

import re
import misc.arguments as args
import tensorflow as tf

from .. import Setup
from .. import struct

class CActivation(struct.CLayer):
  def __init__(self, Func, Name):
    self._Func = Func
    self._Name = Name


  def copy(self):
    New = CActivation(self._Func, self._Name)
    return New


  def __call__(self, Func = args.NotSet, Name = args.NotSet):
    New = self.copy()

    if args.isSet(Func):
      self._Func = Func

    if args.isSet(Name):
      self._Name = Name

    return New


  def apply(self, Input):
    Setup.log("* {} Activation function".format(self._Name))

    with tf.variable_scope(self._Name):
      Output = self._Func(Input)
      tensor_name = re.sub('tower_[0-9]*/', '', Output.name)
      tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(Output))

    return Output


