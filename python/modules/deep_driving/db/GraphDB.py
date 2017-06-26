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

def normalizeLabels(Labels):
  OutLabels = []

  Angle      = Labels[0]/1.1 + 0.5                 # Angle  - Range -0.5 .. 0.5 and clamping between 0 and 1
  Angle      = tf.minimum(Angle, 1)
  OutLabels.append(tf.maximum(Angle, 0))

  OutLabels.append(Labels[1]  * 0.17778 + 1.34445) # L      - Range -7 .. -2.5 mapping to 0.1 .. 0.9
  OutLabels.append(Labels[2]  * 0.1149  + 0.6714)  # M      - Range -5 ..  2   mapping to 0.1 .. 0.9
  OutLabels.append(Labels[3]  * 0.17778 - 0.34445) # R      - Range 2.5 .. 7   mapping to 0.1 .. 0.9
  OutLabels.append(Labels[4]  / 95.0    + 0.12)    # DistL  - Range  0 ..  90  mapping to 0.1 .. 0.9
  OutLabels.append(Labels[5]  / 95.0    + 0.12)    # DistR  - Range  0 ..  90  mapping to 0.1 .. 0.9

  OutLabels.append(Labels[6]  * 0.14545 + 1.40909) # LL     - Range -9 .. -3.5 mapping to 0.1 .. 0.9
  OutLabels.append(Labels[7]  * 0.16    + 0.9)     # ML     - Range -5 .. 0    mapping to 0.1 .. 0.9
  OutLabels.append(Labels[8]  * 0.16    + 0.1)     # MR     - Range  0 .. 5    mapping to 0.1 .. 0.9
  OutLabels.append(Labels[9]  * 0.14545 - 0.40909) # RR     - Range 3.5 .. 9   mapping to 0.1 .. 0.9
  OutLabels.append(Labels[10] / 95.0    + 0.12)    # DistLL - Range  0 ..  90  mapping to 0.1 .. 0.9
  OutLabels.append(Labels[11] / 95.0    + 0.12)    # DistMM - Range  0 ..  90  mapping to 0.1 .. 0.9
  OutLabels.append(Labels[12] / 95.0    + 0.12)    # DistRR - Range  0 ..  90  mapping to 0.1 .. 0.9

  OutLabels.append(Labels[13])                     # Fast   - Range  0 .. 1    mapping to   0 .. 1

  return OutLabels


def denormalizeLabels(Labels):
  OutLabels = []

  OutLabels.append((Labels[0]  - 0.5)     * 1.1)      # Angle  - Range 0.05 .. 0.95 mapping to -0.5 .. 0.5

  OutLabels.append((Labels[1]  - 1.34445) / 0.17778)  # L      - Range  0.1 .. 0.9  mapping to   -7 .. -2.5
  OutLabels.append((Labels[2]  - 0.6714)  / 0.1149)   # M      - Range  0.1 .. 0.9  mapping to   -5 .. 2
  OutLabels.append((Labels[3]  + 0.34445) / 0.17778)  # R      - Range  0.1 .. 0.9  mapping to  2.5 .. 7
  OutLabels.append((Labels[4]  - 0.12)    * 95.0)     # DistL  - Range  0.1 .. 0.9  mapping to    0 .. 90
  OutLabels.append((Labels[5]  - 0.12)    * 95.0)     # DistR  - Range  0.1 .. 0.9  mapping to    0 .. 90

  OutLabels.append((Labels[6]  - 1.40909) / 0.14545)  # LL     - Range  0.1 .. 0.9  mapping to   -9 .. -3.5
  OutLabels.append((Labels[7]  - 0.9)     / 0.16)     # ML     - Range  0.1 .. 0.9  mapping to   -5 .. 0
  OutLabels.append((Labels[8]  - 0.1)     / 0.16)     # MR     - Range  0.1 .. 0.9  mapping to    0 .. 5
  OutLabels.append((Labels[9]  + 0.40909) / 0.14545)  # RR     - Range  0.1 .. 0.9  mapping to  3.5 .. 9
  OutLabels.append((Labels[10] - 0.12)    * 95.0)     # DistLL - Range  0.1 .. 0.9  mapping to    0 .. 90
  OutLabels.append((Labels[11] - 0.12)    * 95.0)     # DistMM - Range  0.1 .. 0.9  mapping to    0 .. 90
  OutLabels.append((Labels[12] - 0.12)    * 95.0)     # DistRR - Range  0.1 .. 0.9  mapping to    0 .. 90

  OutLabels.append(Labels[13])                        # Fast   - Range    0 .. 1    mapping to    0 .. 1

  return OutLabels


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

  Inputs = [
    Image,                                     # 0
    tf.reshape(Features['Angle'],  shape=[1]), # 1

    tf.reshape(Features['L'],      shape=[1]), # 2
    tf.reshape(Features['M'],      shape=[1]), # 3
    tf.reshape(Features['R'],      shape=[1]), # 4
    tf.reshape(Features['DistL'],  shape=[1]), # 5
    tf.reshape(Features['DistR'],  shape=[1]), # 6

    tf.reshape(Features['LL'],     shape=[1]), # 7
    tf.reshape(Features['ML'],     shape=[1]), # 8
    tf.reshape(Features['MR'],     shape=[1]), # 9
    tf.reshape(Features['RR'],     shape=[1]), # 10
    tf.reshape(Features['DistLL'], shape=[1]), # 11
    tf.reshape(Features['DistMM'], shape=[1]), # 12
    tf.reshape(Features['DistRR'], shape=[1]), # 13

    tf.reshape(Features['Fast'],   shape=[1]), # 14
  ]

  return Inputs