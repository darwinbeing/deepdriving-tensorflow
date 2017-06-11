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

import debug

class CTable():
  def __init__(self, Header):
    self._Columns = len(Header)
    self._Header  = tf.constant(shape=[1, int(self._Columns)], dtype=tf.string, value=Header)
    self._Lines   = [self._Header]
    self._Table   = None
    debug.Assert(self._Columns > 0, "There are at least 1 header field required for a table.")


  def addLine(self, Line=[]):
    debug.Assert(self._Columns == len(Line), "You need exact the same number of Line-Elements than Header-Elements!")
    Columns = []
    for Field in Line:
      if isinstance(Field, str):
        Columns.append(tf.constant(shape=[1], dtype=tf.string, value=[Field]))

      else:
        if len(Field.shape) == 2:
          Columns.append(tf.reshape(tf.as_string(Field[0, 0]), shape=[1]))
        elif len(Field.shape) == 1:
          Columns.append(tf.reshape(tf.as_string(Field[0]), shape=[1]))
        elif len(Field.shape) == 0:
          Columns.append(tf.reshape(tf.as_string(Field), shape=[1]))
        else:
          debug.LogError("Don't know how to handle this tensor shape {}".format(Field.shape))

    Line = tf.stack(Columns, axis=1)
    self._Lines.append(Line)


  def build(self):
    if self._Table == None:
      NumberOfLines = len(self._Lines)
      self._Table = tf.reshape(tf.stack(self._Lines, axis=0), shape=[NumberOfLines, self._Columns])

    return self._Table