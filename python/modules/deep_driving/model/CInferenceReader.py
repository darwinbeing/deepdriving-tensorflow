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
import deep_learning as dl
import tensorflow as tf
import cv2

from .. import db

class CInferenceReader(dl.data.CReader):
  def __init__(self, Settings, IsTraining, UsePreprocessing, ForceDataAugmentation):
    self._BatchesInQueue = 0
    self._ImageShape = [Settings['Data']['ImageHeight'], Settings['Data']['ImageWidth'], 3]
    self._NetInputs = {
      "RawImage": None
    }
    self._Outputs = {
      "Image":      None,
      "Labels":     tf.split(tf.placeholder(dtype=tf.int32, shape=[1, 14], name="Label"), 14, axis=1),
      "IsTraining": tf.placeholder(dtype=tf.bool, name="IsTraining"),
      "Lambda":     tf.placeholder(dtype=tf.float32, name="Lambda")
    }

    super().__init__(Settings, IsTraining, UsePreprocessing, ForceDataAugmentation)


  def _build(self, Settings):
    self._NetInputs["RawImage"] = tf.placeholder(dtype=tf.uint8, shape=self._ImageShape)
    Image = self._NetInputs["RawImage"]

    Image = tf.cast(Image, tf.float32, name="Image") / 255.0

    Blue, Green, Red = tf.split(Image, 3, axis=2)
    Image = tf.concat([Red, Green, Blue], axis=2)

    if self._UsePreprocessing:
      with tf.name_scope("Preprocessing"):

        print("* Perform per-pixel normalization")

        MeanReader = dl.data.CMeanReader()
        MeanReader.read(Settings['PreProcessing']['MeanFile'])

        MeanImage = tf.image.resize_images(MeanReader.MeanImage, size=(int(Image.shape[0]), int(Image.shape[1])))
        Image = tf.subtract(Image, MeanImage)

    Image = tf.reshape(Image, shape=[1] + self._ImageShape)

    self._Outputs["Image"] = Image
    return Image


  def _getOutputs(self, Inputs):
    return self._Outputs


  def readSingle(self, Session, Inputs):
    Image = Inputs[0]
    if Image.shape[0] != self._ImageShape[0] or Image.shape[1] != self._ImageShape[1]:
      Image = cv2.resize(Image, (self._ImageShape[1], self._ImageShape[0]))

    return {
      self._NetInputs['RawImage']: Image,
      self._Outputs['IsTraining']: self._IsTraining,
      self._Outputs['Lambda']:     0.0
    }
