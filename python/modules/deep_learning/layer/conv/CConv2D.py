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
import misc.arguments as args
import debug

from .. import struct
from .. import initializer
from .. import Setup
from ... import helpers

class CConv2D(struct.CNamedLayer):
  def __init__(self, Kernel, Filters, Stride = 1, Padding = "SAME", Groups = 1, Name = "Conv2D"):
    super().__init__(Name)
    self._Kernel  = Kernel
    self._Filters = Filters
    self._Stride  = Stride
    self._Padding = Padding
    self._Groups  = Groups
    self._KernelLR = 1.0
    self._BiasLR = 1.0
    self._KernelDecay = 1.0
    self._BiasDecay = 0.0
    self._UseBias = True
    self._KernelInit = initializer.XavierInitializerConv()
    self._BiasInit   = initializer.ConstantInitializer(0.0)

  def copy(self):
    New = CConv2D(Kernel=self._Kernel, Filters=self._Filters)
    New = self._copyArgs(New)
    return New


  def _copyArgs(self, New):
    New = super()._copyArgs(New)
    New._Kernel      = self._Kernel
    New._Filters     = self._Filters
    New._Stride      = self._Stride
    New._Padding     = self._Padding
    New._Groups      = self._Groups
    New._KernelLR    = self._KernelLR
    New._BiasLR      = self._BiasLR
    New._KernelDecay = self._KernelDecay
    New._BiasDecay   = self._BiasDecay
    New._KernelInit  = self._KernelInit
    New._BiasInit    = self._BiasInit
    New._UseBias     = self._UseBias
    return New


  def __call__(self, Kernel = args.NotSet, Filters = args.NotSet, Stride = args.NotSet, Padding = args.NotSet, Groups = args.NotSet, Name = args.NotSet):
    New = super().__call__(Name)

    if args.isSet(Kernel):
      New._Kernel = Kernel

    if args.isSet(Filters):
      New._Filters = Filters

    if args.isSet(Stride):
      New._Stride = Stride

    if args.isSet(Padding):
      New._Padding = Padding

    if args.isSet(Groups):
      New._Groups = Groups

    return New


  def setKernel(self, Kernel):
    self._Kernel = Kernel
    return self

  def setFilters(self, Filters):
    self._Filters = Filters
    return self

  def setStride(self, Stride):
    self._Stride = Stride
    return self

  def setPadding(self, Padding):
    self._Padding = Padding
    return self

  def setGroups(self, Groups):
    self._Groups = Groups
    return self

  def setKernelLR(self, LR):
    self._KernelLR = LR
    return self

  def setBiasLR(self, LR):
    self._BiasLR = LR
    return self

  def setKernelDecay(self, Decay):
    self._KernelDecay = Decay
    return self

  def setBiasDecay(self, Decay):
    self._BiasDecay = Decay
    return self

  def setKernelInit(self, Init):
    self._KernelInit = Init
    return self

  def setBiasInit(self, Init):
    self._BiasInit = Init
    return self

  def setUseBias(self, UseBias):
    self._UseBias = UseBias
    return self

  def _apply(self, Input):
    Temp = self.copy()

    debug.Assert(Temp._Kernel  != None, "You have to specify the kernel of this convolution layer.")
    debug.Assert(Temp._Filters != None, "You have to specify the number of filters of this convolution layer.")

    InputChannels = int(Input.shape[3])

    debug.Assert(InputChannels % Temp._Groups == 0, "Canno divide input channels by number of groups wihtout Rest!")
    debug.Assert(Temp._Filters % Temp._Groups == 0, "Canno divide output channels by number of groups wihtout Rest!")

    if isinstance(Temp._Kernel, int):
      KernelShape = [int(Temp._Kernel), int(Temp._Kernel), int(InputChannels/Temp._Groups), int(Temp._Filters)]
    else:
      KernelShape = [int(Temp._Kernel[0]), int(Temp._Kernel[1]), int(InputChannels/Temp._Groups), int(Temp._Filters)]

    Setup.log("* Kernel {}x{}".format(KernelShape[0], KernelShape[1]))

    if isinstance(Temp._Stride, int):
      StrideShape = [1, int(Temp._Stride), int(Temp._Stride), 1]
    else:
      StrideShape = [1, int(Temp._Stride[0]), int(Temp._Stride[1]), 1]

    Setup.log("* Stride {}x{}".format(StrideShape[1], StrideShape[2]))

    if isinstance(Temp._Padding, int):
      Setup.log("* Use {} Padding pixel".format(Temp._Padding))
      Input = tf.pad(Input, [[0, 0], [Temp._Padding, Temp._Padding], [Temp._Padding, Temp._Padding], [0, 0]], "SYMMETRIC")
      Padding = "VALID"

    else:
      Padding = Temp._Padding

    Setup.log("* Padding {}".format(Padding))

    if Temp._KernelLR != 1.0:
      Setup.log("* Kernel-LR: {}".format(Temp._KernelLR))

    if Temp._KernelDecay != 1.0:
      Setup.log("* Kernel-Decay: {}".format(Temp._KernelDecay))

    Setup.log("* Kernel-Initializer: {}".format(Temp._KernelInit))

    Kernel = helpers.createKernel2D(Shape=KernelShape,
                                    Initializer=Temp._KernelInit.getInit(),
                                    WeightDecayFactor=Temp._KernelDecay,
                                    LearningRate=Temp._KernelLR)

    if Temp._UseBias:
      if Temp._BiasLR != 1.0:
        Setup.log("* Bias-LR: {}".format(Temp._BiasLR))

      if Temp._BiasDecay != 1.0:
        Setup.log("* Bias-Decay: {}".format(Temp._BiasDecay))

      Setup.log("* Bias-Initializer: {}".format(Temp._BiasInit))

      Bias   = helpers.createBias(Shape=[Temp._Filters],
                                  Name="Bias",
                                  Initializer=Temp._BiasInit.getInit(),
                                  WeightDecayFactor=Temp._BiasDecay,
                                  LearningRate=Temp._BiasLR)

    if Temp._Groups <= 1:
      Output = tf.nn.conv2d(input=Input, filter=Kernel, strides=StrideShape, padding=Padding)
      if Temp._UseBias:
        Output = tf.nn.bias_add(Output, Bias)

    else:
      # The basic idea of this group implementation is taken from the caffe-2-tensorflow
      # generator at: https://github.com/ethereon/caffe-tensorflow
      # Copyright (c) 2016 Saumitro Dasgupta (also MIT License)

      Setup.log("* Groups {}".format(Temp._Groups))
      Setup.increaseLoggerIndent(2)
      InputGroups  = tf.split(Input,  Temp._Groups, 3)
      KernelGroups = tf.split(Kernel, Temp._Groups, 3)
      OutputGroups = []
      for i in range(Temp._Groups):
        Setup.log("* Group[{}]: Input {}, Kernel {}".format(i, InputGroups[i].shape, KernelGroups[i].shape))
        SingleOutput = tf.nn.conv2d(input=InputGroups[i],
                                    filter=KernelGroups[i],
                                    strides=StrideShape,
                                    padding=Padding)

        if Temp._UseBias:
          SingleOutput = tf.nn.bias_add(SingleOutput, Bias)

        OutputGroups.append(SingleOutput)

      Output = tf.concat(OutputGroups, 3)
      Setup.decreaseLoggerIndent(2)

    if Setup.StoreHistogram:
      tf.summary.histogram("Kernel", Kernel)
      if Temp._UseBias:
        tf.summary.histogram("Bias",  Bias)
      tf.summary.histogram("Output",  Output)

    if Temp._UseBias:
      Setup.log("* with Output-Shape {}".format(Output.shape))
    else:
      Setup.log("* with Output-Shape {} without Bias".format(Output.shape))

    return Output