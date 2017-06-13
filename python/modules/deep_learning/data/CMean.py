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
import numpy as np

def getInt64Feature(Value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[Value]))

def getFloatFeature(Value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=[Value]))

def getByteFeature(Value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[Value]))

class CMeanReader():
  def __init__(self):
    self._MeanImage = None
    self._VarImage  = None
    self._MeanColor = None
    self._VarColor  = None


  def store(self, Filename, MeanImage, VarImage, MeanColor, VarColor):
    Writer = tf.python_io.TFRecordWriter(path=Filename)

    Features = tf.train.Features(feature={
      'Width':     getInt64Feature(MeanImage.shape[1]),
      'Height':    getInt64Feature(MeanImage.shape[0]),
      'Channels':  getInt64Feature(MeanImage.shape[2]),

      'MeanImage': getByteFeature(MeanImage.tostring()),
      'VarImage':  getByteFeature(VarImage.tostring()),
      'MeanColor': getByteFeature(MeanColor.tostring()),
      'VarColor':  getByteFeature(VarColor.tostring()),
    })

    Record = tf.train.Example(features=Features)
    Writer.write(Record.SerializeToString())


  def read(self, Filename):
    RecordIterator = tf.python_io.tf_record_iterator(path=Filename)

    for Record in RecordIterator:
      Example = tf.train.Example()
      Example.ParseFromString(Record)

      Width    = Example.features.feature['Width'].int64_list.value[0]
      Height   = Example.features.feature['Height'].int64_list.value[0]
      Channels = Example.features.feature['Channels'].int64_list.value[0]

      ImageShape = (Height, Width, Channels)
      ColorShape = (Channels)
      print("Read mean-image with shape {}".format(ImageShape))

      RawMeanImage = Example.features.feature['MeanImage'].bytes_list.value[0]
      RawVarImage  = Example.features.feature['VarImage'].bytes_list.value[0]
      RawMeanColor = Example.features.feature['MeanColor'].bytes_list.value[0]
      RawVarColor  = Example.features.feature['VarColor'].bytes_list.value[0]

      self._MeanImage = np.fromstring(RawMeanImage, dtype=np.float32).reshape(ImageShape)
      self._VarImage  = np.fromstring(RawVarImage, dtype=np.float32).reshape(ImageShape)
      self._MeanColor = np.fromstring(RawMeanColor, dtype=np.float32).reshape(ColorShape)
      self._VarColor  = np.fromstring(RawVarColor, dtype=np.float32).reshape(ColorShape)



  @property
  def MeanImage(self):
    return self._MeanImage

  @property
  def VarImage(self):
    return self._VarImage

  @property
  def MeanColor(self):
    return self._MeanColor

  @property
  def VarColor(self):
    return self._VarColor