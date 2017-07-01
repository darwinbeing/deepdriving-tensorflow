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

class CInitializer():
  def __init__(self, TFInit, Name):
    self._TFInit   = TFInit
    self._Name     = Name
    self._FullInit = None
    self._InitArgs = {}
    self._InitArgList = []

  def __call__(self, *args, **kwargs):
    self._InitArgs = kwargs
    self._InitArgList = args
    self._FullInit = self._TFInit(*args, **kwargs)
    return self

  def getInit(self):
    return self._FullInit

  def __str__(self):
    String = self._Name
    String += "("

    ArgStrings = []
    for Key, Value in self._InitArgs.items():
      ArgStrings.append("{} = {}".format(Key, Value))

    for Value in self._InitArgList:
      ArgStrings.append("{}".format(Value))

    for i, ArgString in enumerate(ArgStrings):
      String += ArgString
      if i < len(ArgStrings)-1:
        String += ", "

    String += ")"
    return String


XavierInitializerConv = CInitializer(tf.contrib.layers.xavier_initializer_conv2d, "XavierInitializerConv")
XavierInitializer     = CInitializer(tf.contrib.layers.xavier_initializer, "XavierInitializer")
NormalInitializer     = CInitializer(tf.truncated_normal_initializer, "NormalInitializer")
ConstantInitializer   = CInitializer(tf.constant_initializer, "ConstantInitializer")

