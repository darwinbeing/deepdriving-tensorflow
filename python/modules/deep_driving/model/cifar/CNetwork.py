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

    Scope = "Network"
    with tf.variable_scope(Scope):
      self.log("Creating network Graph...")

      Input = Inputs['Image']
      Output = Input

      self.log(" * network Input-Shape: {}".format(Input.shape))

      Output = self._buildNetwork(Input)

      self.log(" * network Output-Shape: {}".format(Output.shape))

      Variables, Tensors = dl.helpers.getTrainableVariablesInScope(Scope)
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
    dl.layer.Setup.setupKernelInitializer(dl.helpers.NormalInitializer(mean=0, stddev=5e-2))
    dl.layer.Setup.setupBiasInitializer(dl.helpers.ConstantInitializer(0.0))

    # We instantiate all variables using tf.get_variable() instead of
    # tf.Variable() in order to share variables across multiple GPU training runs.
    # If we only ran this model on a single GPU, we could simplify this function
    # by replacing all instances of tf.get_variable() with tf.Variable().
    #
    # conv1
    with tf.variable_scope('conv1') as scope:
      conv1 = dl.layer.createConvolution2d(images, Size=5, Filters=64, WeightDecay=0.0)
      act1           = dl.layer.createActivation(conv1, Func="ReLU")
      dl.helpers.saveFeatureMap(act1, "Features")
      pool1          = dl.layer.createPooling(act1, Size=3, Stride=2, Pool="MAX")
      norm1          = dl.layer.createLRN(pool1, Radius=4, Alpha=0.001 / 9.0, Beta = 0.75)


    dl.layer.Setup.setupBiasInitializer(dl.helpers.ConstantInitializer(0.1))

    # conv2
    with tf.variable_scope('conv2') as scope:
      conv2 = dl.layer.createConvolution2d(norm1, Size=5, Filters=64, WeightDecay=0.0)
      act2           = dl.layer.createActivation(conv2, Func="ReLU")
      dl.helpers.saveFeatureMap(act2, "Features")
      norm2          = dl.layer.createLRN(act2, Radius=4, Alpha=0.001 / 9.0, Beta = 0.75)
      pool2          = dl.layer.createPooling(norm2, Size=3, Stride=2, Pool="MAX")


    dl.layer.Setup.setupWeightInitializer(dl.helpers.NormalInitializer(mean=0, stddev=0.04))

    # local3
    with tf.variable_scope('local3') as scope:
      local3 = dl.layer.createFullyConnected(pool2, Size=384, Func="ReLU")


    # local4
    with tf.variable_scope('local4') as scope:
      weights = _variable_with_weight_decay('weights', shape=[384, 192],
                                            stddev=0.04, wd=1.0)
      biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))
      local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)
      _activation_summary(local4)

    NUM_CLASSES = 10
    # linear layer(WX + b),
    # We don't apply softmax here because
    # tf.nn.sparse_softmax_cross_entropy_with_logits accepts the unscaled logits
    # and performs the softmax internally for efficiency.
    with tf.variable_scope('softmax_linear') as scope:
      weights = _variable_with_weight_decay('weights', [192, NUM_CLASSES],
                                              stddev=1 / 192.0, wd=0.0)
      biases = _variable_on_cpu('biases', [NUM_CLASSES],
                                  tf.constant_initializer(0.0))
      softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)
      _activation_summary(softmax_linear)

    return softmax_linear