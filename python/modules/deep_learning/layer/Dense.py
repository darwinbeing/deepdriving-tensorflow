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

from .. import helpers

from .Setup import _LOG, _INITIALIZER
from .Activation import createActivation

def createDense(Input, Size, Name="Dense", WeightDecay = 1.0):
  Size = int(Size)

  def create(Input, Size, WeightDecay):
    InputShape = Input.shape
    if len(InputShape) > 2:
      InputLength = int(np.prod(InputShape[1:]))
      _LOG("   * Reshape layer input {} to vector with {} elements.".format(InputShape, InputLength))
      Input = tf.reshape(Input, shape=[-1, InputLength])

    else:
      InputLength = int(InputShape[1])

    X = Input
    W = helpers.createVariable(Shape=[InputLength, Size], Name="Weights", WeightDecayFactor=WeightDecay, Initializer=_INITIALIZER['Weights'])
    B = helpers.createBias(Shape=[Size], Name="Bias", Initializer=_INITIALIZER['Bias'])
    return tf.add(tf.matmul(X, W), B, name="Signal")

  if Name != None:
    _LOG(" * Create Dense-Layer \"{}\" with {} output-nodes.".format(Name, Size))
    with tf.name_scope(Name):
      Signal = create(Input, Size, WeightDecay)

  else:
    Signal = create(Input, Size, WeightDecay)

  return Signal


def createFullyConnected(Input, Size, Func="ReLU", Name="FC", WeightDecay=1.0):
  Output = Input

  with tf.name_scope(Name):
    _LOG(" * Create Fully-Connected-Layer \"{}\" with {} output-nodes.".format(Name, Size))
    _LOG("   * With Activation {}".format(Func))
    Output = createDense(Input=Output, Size=Size, Name=None, WeightDecay=WeightDecay)
    Output = createActivation(Input=Output, Func=Func)

  return Output
