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

def buildFeatureParser(SerializedExample):
  Features = tf.parse_single_example(
    SerializedExample,
    features={
      'ImageWidth':    tf.FixedLenFeature([], tf.int64),
      'ImageHeight':   tf.FixedLenFeature([], tf.int64),
      'ImageChannels': tf.FixedLenFeature([], tf.int64),
      'Image':         tf.FixedLenFeature([], tf.string),

      # Data for managing the different tracks
      'TrackName':     tf.FixedLenFeature([], tf.string),
      'TrackID':       tf.FixedLenFeature([], tf.int64),
      'RaceID':        tf.FixedLenFeature([], tf.int64),
      'FrameNumber':   tf.FixedLenFeature([], tf.int64),

      # Additional data
      'Speed':         tf.FixedLenFeature([], tf.float32),
      'Lanes':         tf.FixedLenFeature([], tf.int64),

      # Original Labels
      'Angle':         tf.FixedLenFeature([], tf.float32),
      'Fast':          tf.FixedLenFeature([], tf.float32),
      'LL':            tf.FixedLenFeature([], tf.float32),
      'ML':            tf.FixedLenFeature([], tf.float32),
      'MR':            tf.FixedLenFeature([], tf.float32),
      'RR':            tf.FixedLenFeature([], tf.float32),
      'DistLL':        tf.FixedLenFeature([], tf.float32),
      'DistMM':        tf.FixedLenFeature([], tf.float32),
      'DistRR':        tf.FixedLenFeature([], tf.float32),
      'L':             tf.FixedLenFeature([], tf.float32),
      'M':             tf.FixedLenFeature([], tf.float32),
      'R':             tf.FixedLenFeature([], tf.float32),
      'DistL':         tf.FixedLenFeature([], tf.float32),
      'DistR':         tf.FixedLenFeature([], tf.float32),
    }
  )

  ImageWidth       = tf.cast(Features['ImageWidth'], tf.int32)
  ImageHeigth      = tf.cast(Features['ImageHeight'], tf.int32)
  Image            = tf.decode_raw(Features['Image'], tf.uint8)
  Image            = tf.reshape(Image, tf.stack([ImageHeigth, ImageWidth, 3]))
  Image            = tf.cast(Image, tf.float32, name="Image")/255.0

  Blue, Green, Red = tf.split(Image, 3, axis=2)
  Image = tf.concat([Red, Green, Blue], axis=2)

  Angle = Features['Angle']/1.1 + 0.5 # Range -0.5 .. 0.5 and clamping between 0 and 1
  Angle = tf.minimum(Angle, 1)
  Angle = tf.maximum(Angle, 0)

  Inputs = [
    Image,                          # 0
    tf.reshape(Angle,                          shape=[1]), # 1
    tf.reshape(Features['Fast']*0.6 + 0.2,     shape=[1]), # 2  - Range  0 .. 1    mapping to 0.2 .. 0.8
    tf.reshape(Features['LL']*0.14545+1.40909, shape=[1]), # 3  - Range -9 .. -3.5 mapping to 0.1 .. 0.9
    tf.reshape(Features['ML']*0.16   +0.9,     shape=[1]), # 4  - Range -5 .. 0    mapping to 0.1 .. 0.9
    tf.reshape(Features['MR']*0.16   +0.1,     shape=[1]), # 5  - Range  0 .. 5    mapping to 0.1 .. 0.9
    tf.reshape(Features['RR']*0.14545-0.40909, shape=[1]), # 6  - Range 3.5 .. 9   mapping to 0.1 .. 0.9
    tf.reshape(Features['DistLL']/112+0.1,     shape=[1]), # 7  - Range  0 ..  90  mapping to 0.1 .. 0.9
    tf.reshape(Features['DistMM']/112+0.1,     shape=[1]), # 8  - Range  0 ..  90  mapping to 0.1 .. 0.9
    tf.reshape(Features['DistRR']/112+0.1,     shape=[1]), # 9  - Range  0 ..  90  mapping to 0.1 .. 0.9
    tf.reshape(Features['L']*0.17778+1.34445,  shape=[1]), # 10 - Range -7 .. -2.5 mapping to 0.1 .. 0.9
    tf.reshape(Features['M']*0.1149 +0.6714,   shape=[1]), # 11 - Range -5 ..  2   mapping to 0.1 .. 0.9
    tf.reshape(Features['R']*0.17778-0.34445,  shape=[1]), # 12 - Range 2.5 .. 7   mapping to 0.1 .. 0.9
    tf.reshape(Features['DistL']/112+0.1,      shape=[1]), # 13 - Range  0 ..  90  mapping to 0.1 .. 0.9
    tf.reshape(Features['DistR']/112+0.1,      shape=[1]), # 14 - Range  0 ..  90  mapping to 0.1 .. 0.9
  ]

  return Inputs