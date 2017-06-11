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

import math
import tensorflow as tf

import debug

from .. import layer

def saveFeatureMap(Features, Name="FeatureMap"):
  # Taken from: https://stackoverflow.com/questions/33802336/visualizing-output-of-convolutional-layer-in-tensorflow

  if layer.Setup.StoreFeatureMap:
    Name = tf.contrib.framework.get_name_scope() + "/" + Name
    BatchSize   = int(Features.shape[0])
    ImageHeight = int(Features.shape[1])+4
    ImageWidth  = int(Features.shape[2])+4
    Maps        = int(Features.shape[3])

    FirstSample = Features[0,:,:,:]
    WithBorder  = tf.image.resize_image_with_crop_or_pad(FirstSample, ImageHeight, ImageWidth)

    BestY = 1
    Y = 1
    while True:
      X = int(Maps/Y)
      if (X*Y) == Maps:
        if Y > BestY:
          BestY = Y
          if X <= Y:
            break
      Y += 1

    Y = int(BestY)
    X = int(Maps/Y)
    debug.Assert(Y*X == Maps, "Cannot find two factors to split the number of maps {}.".format(Maps))

    FeatureImage = tf.reshape(WithBorder, shape=[ImageHeight, ImageWidth, Y, X])
    FeatureImage = tf.transpose(FeatureImage, perm=[2, 0, 3, 1]) # get tensor [Y, ImageHeight, X, ImageWidth]
    FeatureImage = tf.reshape(FeatureImage, shape=[1, Y*ImageHeight, X*ImageWidth, 1])

    tf.summary.image(Name, FeatureImage)