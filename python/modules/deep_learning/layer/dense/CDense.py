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

import copy
import numpy as np
import tensorflow as tf
import misc.arguments as args
import debug

from .. import struct
from .. import initializer
from .. import Setup
from ... import helpers

class CDense(struct.CNamedLayer):

  _Nodes = None
  _WeightLR    = 1.0
  _BiasLR      = 1.0
  _WeightDecay = 1.0
  _BiasDecay   = 0.0
  _WeightInit  = None
  _BiasInit    = None
  _UseBN       = False
  def __init__(self, Nodes, Name = "Dense"):
    super().__init__(Name)
    self._Nodes = Nodes
    self._WeightInit = initializer.XavierInitializer()
    self._BiasInit = initializer.ConstantInitializer(0.0)


  def copy(self):
    New = CDense(self._Nodes)
    New = self._copyArgs(New)
    return New


  def _copyArgs(self, New):
    New = super()._copyArgs(New)
    New._Nodes       = self._Nodes
    New._WeightLR    = self._WeightLR
    New._BiasLR      = self._BiasLR
    New._WeightDecay = self._WeightDecay
    New._BiasDecay   = self._BiasDecay
    New._WeightInit  = self._WeightInit
    New._BiasInit    = self._BiasInit
    New._UseBN       = self._UseBN
    return New


  def __call__(self, Nodes = args.NotSet, Name = args.NotSet):
    New = super().__call__(Name)

    if args.isSet(Nodes):
      New._Nodes = Nodes

    return New


  def setWeightLR(self, LR):
    self._WeightLR = LR
    return self

  def setBiasLR(self, LR):
    self._BiasLR = LR
    return self

  def setWeightDecay(self, Decay):
    self._WeightDecay = Decay
    return self

  def setBiasDecay(self, Decay):
    self._BiasDecay = Decay
    return self

  def setWeightInit(self, Init):
    self._WeightInit = Init
    return self

  def setBiasInit(self, Init):
    self._BiasInit = Init
    return self

  def setUseBN(self, UseBN):
    self._UseBN = UseBN
    return self


  def _apply(self, Input):
    Temp = self.copy()

    debug.Assert(Temp._Nodes != None, "You have to specify the number of nodes for this layer.")

    InputShape = Input.shape
    if len(InputShape) > 2:
      InputLength = int(np.prod(InputShape[1:]))
      Setup.log("* Reshape layer input {} to vector with {} elements.".format(InputShape, InputLength))
      Input = tf.reshape(Input, shape=[-1, InputLength])

    else:
      InputLength = int(InputShape[1])

    Setup.log("* with {} Output-Nodes".format(Temp._Nodes))

    X = Input
    W = helpers.createVariable(Shape=[InputLength, Temp._Nodes],
                               Name="Weights",
                               WeightDecayFactor=Temp._WeightDecay,
                               #Initializer=Temp._WeightInit,
                               Initializer=self._WeightInit,
                               LearningRate=Temp._WeightLR)

    if not Temp._UseBN:
      B = helpers.createBias(Shape=[Temp._Nodes],
                             Name="Bias",
                             WeightDecayFactor=Temp._BiasDecay,
                             #Initializer=Temp._BiasInit,
                             LearningRate=Temp._BiasLR)

    S = tf.matmul(X, W)

    if not Temp._UseBN:
      S = tf.add(S, B)
    else:
      Setup.log("* and Batch-Normalization")

    if Setup.StoreHistogram:
      tf.summary.histogram("Weights", W)
      if not Temp._UseBN:
        tf.summary.histogram("Bias",  B)
      tf.summary.histogram("Signal",  S)

    return S