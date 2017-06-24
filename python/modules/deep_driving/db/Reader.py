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

import numpy as np
import debug
import tensorflow as tf

from .Common import getDBFilenames

class CDBReader():
  def __init__(self, DatabasePath):
    self._Files = getDBFilenames(DatabasePath)
    debug.Assert(len(self._Files) > 0, "There are no tfrecord files in path {}.".format(DatabasePath))
    self._Iterator = None
    self._Image = None


  def next(self):
    if self._Iterator is None:
      self._getNextIterator()

    if self._Iterator is None:
      return False

    else:
      Record = next(self._Iterator, None)
      while Record is None:
        self._getNextIterator()
        if self._Iterator is None:
          return False
        Record = next(self._getNextIterator())

      self._readRecord(Record)
      return True


  def _readRecord(self, Record):
    Example = tf.train.Example()
    Example.ParseFromString(Record)

    ImageWidth    = int(Example.features.feature['ImageWidth'].int64_list.value[0])
    ImageHeight   = int(Example.features.feature['ImageHeight'].int64_list.value[0])
    ImageChannels = int(Example.features.feature['ImageChannels'].int64_list.value[0])
    RawImage      = Example.features.feature['Image'].bytes_list.value[0]

    Image = np.fromstring(RawImage, dtype=np.uint8)
    Image = Image.reshape((ImageHeight, ImageWidth, ImageChannels))
    self._Image = Image


  def _getNextIterator(self):
    if len(self._Files) > 0:
      File = self._Files.pop(0)
      self._Iterator = tf.python_io.tf_record_iterator(File)


  @property
  def Image(self):
    return self._Image