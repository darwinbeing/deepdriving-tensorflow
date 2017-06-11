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

from .. import helpers

from .Setup import Setup
from .Activation import createActivation


def createConvolution2d(Input, Size, Filters, Stride = 1, Name="Conv2D", WeightDecay=1.0, Padding="SAME"):
  InputChannels = int(Input.shape[3])
  KernelShape   = [int(Size), int(Size), InputChannels, int(Filters)]
  StrideShape   = [1, int(Stride), int(Stride), 1]

  def create(Input, KernelShape, Filters, StrideShape, Padding, WeightDecay):
    Kernel = helpers.createKernel2D(Shape=KernelShape, Initializer=Setup.Initializer['Kernel2D'], WeightDecayFactor=WeightDecay)
    Bias   = helpers.createBias(Shape=[Filters], Name="Bias", Initializer=Setup.Initializer['Bias'])

    Output = Input
    Output = tf.nn.conv2d(input=Output, filter=Kernel, strides=StrideShape, padding=Padding)
    Output = tf.nn.bias_add(Output, Bias)

    tf.summary.histogram("Kernel", Kernel)
    tf.summary.histogram("Bias",   Bias)
    tf.summary.histogram("Signal", Output)

    return Output

  if Name != None:
    with tf.name_scope(Name):
      Setup.Log(" * Create Conv2D Layer {} with Kernel {}, Stride {}, Padding \"{}\" and {} Feature Maps".format(Name, Size, Stride, Padding, Filters))
      Output = create(Input, KernelShape, Filters, StrideShape, Padding, WeightDecay)

  else:
    Setup.Log("   * Conv2D: Kernel {}; Stride {}; Padding {}; Feature-Maps {}".format(Size, Stride, Padding, Filters))
    Output = create(Input, KernelShape, Filters, StrideShape, Padding, WeightDecay)

  return Output



def createPooling(Input, Size = 3, Stride = 2, Pool="MAX", Name="Pooling", Padding="SAME"):
  WindowShape = [1, int(Size),   int(Size), 1]
  StrideShape = [1, int(Stride), int(Stride), 1]

  def create(Input, WindowShape, StrideShape, Padding, Pool):
    if Pool == "MAX" or Pool == "max":
      Output = tf.nn.max_pool(Input, ksize=WindowShape, strides=StrideShape, padding=Padding)

    elif Pool == "AVG" or Pool == "avg":
      Output = tf.nn.avg_pool(Input, ksize=WindowShape, strides=StrideShape, padding=Padding)

    else:
      debug.LogError("Unknown Pooling-Function \"{}\".".format(Pool))

    return Output


  if Name != None:
    with tf.name_scope(Name):
      Setup.Log(" * Create Pooling Layer {} with Window {}, Stride {}, Padding \"{}\" and Function {} ".format(Name, Size, Stride, Padding, Pool))
      Output = create(Input, WindowShape, StrideShape, Padding, Pool)

  else:
    Setup.Log("   * Pooling: Window {}; Stride {}; Padding {}; Function {}".format(Size, Stride, Padding, Pool))
    Output = create(Input, WindowShape, StrideShape, Padding, Pool)

  return Output


def createLRN(Input, LocalSize, Alpha, Beta, Name="LRN"):

  def create(Input, LocalSize, Alpha, Beta):
    return tf.nn.lrn(Input, depth_radius=LocalSize, bias=1, alpha=Alpha, beta=Beta)

  if Name != None:
    with tf.name_scope(Name):
      Setup.Log(" * Create LRN Layer {} with LocalSize {}, Alpha {}, Beta {}".format(Name, LocalSize, Alpha, Beta))
      Output = create(Input, LocalSize, Alpha, Beta)

  else:
    Setup.Log("   * LRN: LocalSize {}; Alpha {}; Beta {}".format(LocalSize, Alpha, Beta))
    Output = create(Input, LocalSize, Alpha, Beta)

  return Output
