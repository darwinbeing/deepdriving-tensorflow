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

import deep_learning as dl
import numpy as np
import tensorflow as tf

from .TutorialHelper import _activation_summary, _variable_with_weight_decay, _variable_on_cpu, FLAGS

class CNetwork(dl.network.CNetwork):
  def _build(self, Inputs, Settings):
    dl.layer.Setup.setupLogger(self.log)
    dl.layer.Setup.setupIsTraining(Inputs['IsTraining'])
    dl.layer.Setup.setupHistogram(False)
    dl.layer.Setup.setupOutputText(True)
    dl.layer.Setup.setupFeatureMap(True)
    dl.layer.Setup.setupStoreSparsity(True)

    self.log("Creating network Graph...")

    Input = Inputs['Image']
    Output = Input

    self.log(" * network Input-Shape: {}".format(Input.shape))

    Output = self._buildNetwork(Input)

    self.log(" * network Output-Shape: {}".format(Output.shape))

    Variables, Tensors = dl.helpers.getTrainableVariablesInScope(dl.helpers.getNameScope())
    self.log("Finished to build network with {} trainable variables in {} tensors.".format(Variables, Tensors))

    Structure = {
      "Input":  Input,
      "Output": Output
    }
    return  Structure


  def _getOutputs(self, Structure):
    return {'Output': Structure['Output']}

## Custom methods

  def _buildNetwork(self, images):
    # We instantiate all variables using tf.get_variable() instead of
    # tf.Variable() in order to share variables across multiple GPU training runs.
    # If we only ran this model on a single GPU, we could simplify this function
    # by replacing all instances of tf.get_variable() with tf.Variable().
    #
    # conv1
    with tf.variable_scope('conv1') as scope:
      conv1a          = dl.layer.createConvolution2d(images, Size=5, Filters=128, WeightDecay=0.0)
      conv1b          = dl.layer.createConvolution2d(conv1a, Size=5, Filters=128, WeightDecay=0.0)
      norm1          = dl.layer.createBatchNormalization(conv1b)
      act1           = dl.layer.createActivation(norm1, Func="ReLU")
      dl.helpers.saveFeatureMap(act1, "Features")
      pool1          = dl.layer.createPooling(act1, Size=3, Stride=2, Pool="MAX")

    # conv2
    with tf.variable_scope('conv2') as scope:
      conv2a          = dl.layer.createConvolution2d(pool1, Size=5, Filters=128, WeightDecay=0.0)
      conv2b          = dl.layer.createConvolution2d(conv2a, Size=5, Filters=128, WeightDecay=0.0)
      norm2          = dl.layer.createBatchNormalization(conv2b)
      act2           = dl.layer.createActivation(norm2, Func="ReLU")
      dl.helpers.saveFeatureMap(act2, "Features")
      pool2          = dl.layer.createPooling(act2, Size=3, Stride=2, Pool="MAX")

    # conv3
    with tf.variable_scope('conv3') as scope:
      conv3a          = dl.layer.createConvolution2d(pool2, Size=5, Filters=128, WeightDecay=0.0)
      conv3b          = dl.layer.createConvolution2d(conv3a, Size=5, Filters=128, WeightDecay=0.0)
      norm3          = dl.layer.createBatchNormalization(conv3b)
      act3           = dl.layer.createActivation(norm3, Func="ReLU")
      dl.helpers.saveFeatureMap(act3, "Features")
      pool3          = dl.layer.createPooling(act3, Size=3, Stride=2, Pool="MAX")

    NumberOfClasses = 10
    Seq = dl.layer.Sequence("Network")

    Seq.add(dl.layer.Dense_BN_ReLU(1024))
    Seq.add(dl.layer.Dropout(0.5))

    Seq.add(dl.layer.Dense_BN_ReLU(256))

    Seq.add(dl.layer.Dense_BN_ReLU(64))

    Seq.add(dl.layer.Dense(NumberOfClasses))

    return Seq.apply(pool3)

    # local4
    #with tf.variable_scope('local4') as scope:
    #  local4 = dl.layer.createFullyConnected(pool3, Size=1024, Func="ReLU")
    #  local4 = dl.layer.createDropout(Input=local4, KeepRatio=0.5, Name="Drop")

    # local5
    #with tf.variable_scope('local5') as scope:
    #  local5 = dl.layer.createFullyConnected(local4, Size=256, Func="ReLU")

    # local6
    #with tf.variable_scope('local6') as scope:
    #  local6 = dl.layer.createFullyConnected(local5, Size=64, Func="ReLU")

    #NUM_CLASSES = 10
    #with tf.variable_scope('softmax_linear') as scope:
    #  softmax_linear = dl.layer.createDense(local6, Size=NUM_CLASSES, WeightDecay=0.0)

    #return softmax_linear