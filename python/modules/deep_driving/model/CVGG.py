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


class CVGG(dl.network.CNetwork):
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

      Input       = Inputs['Image']
      OutputNodes = len(Inputs['Labels'])

      self.log(" * network Input-Shape: {}".format(Input.shape))

      Output = buildVGG(Input, OutputNodes)

      self.log(" * network Output-Shape: {}".format(Output.shape))

      # We have 14 outputs, output 1 is the only probability output, the remaining are regression outputs
      Outputs = tf.split(Output, 14, axis=1)

      for i, O in enumerate(Outputs):
        self.log("   * Output {} has shape {}".format(i, O.shape))

      Variables, Tensors = dl.helpers.getTrainableVariablesInScope(Scope)
      self.log("Finished to build network with {} trainable variables in {} tensors.".format(Variables, Tensors))

    Structure = {
      "Input":  Input,
      "Output": Outputs
    }
    return  Structure


  def _getOutputs(self, Structure):
    return {'Output': Structure['Output']}

## Custom methods


def buildVGG(Input, OutputNodes):
  # Implementation taken from https://github.com/huyng/tensorflow-vgg
  from tensorflow.contrib.layers import xavier_initializer
  from .cifar.TutorialHelper import _variable_with_weight_decay, _variable_on_cpu, _activation_summary

  keep_prob = 0.5

  def conv(input_tensor, name, kw, kh, n_out, dw=1, dh=1, activation_fn=tf.nn.relu):
    n_in = input_tensor.get_shape()[-1].value
    with tf.variable_scope(name):
      weights = tf.get_variable('weights', [kh, kw, n_in, n_out], tf.float32, xavier_initializer())
      biases = tf.get_variable("bias", [n_out], tf.float32, tf.constant_initializer(0.0))
      conv = tf.nn.conv2d(input_tensor, weights, (1, dh, dw, 1), padding='SAME')
      activation = activation_fn(tf.nn.bias_add(conv, biases))

    return activation


  def fully_connected(input_tensor, name, n_out, activation_fn=tf.nn.relu):
    n_in = input_tensor.get_shape()[-1].value
    with tf.variable_scope(name):
      weights = tf.get_variable('weights', [n_in, n_out], tf.float32, xavier_initializer())
      biases = tf.get_variable("bias", [n_out], tf.float32, tf.constant_initializer(0.0))
      logits = tf.nn.bias_add(tf.matmul(input_tensor, weights), biases)

    return activation_fn(logits)


  def pool(input_tensor, name, kh, kw, dh, dw):
    return tf.nn.max_pool(input_tensor,
                          ksize=[1, kh, kw, 1],
                          strides=[1, dh, dw, 1],
                          padding='VALID',
                          name=name)


  net = Input

  # block 1 -- outputs 112x112x64
  net = conv(net, name="conv1_1", kh=3, kw=3, n_out=64)
  net = conv(net, name="conv1_2", kh=3, kw=3, n_out=64)
  net = pool(net, name="pool1",   kh=2, kw=2, dw=2, dh=2)

  # block 2 -- outputs 56x56x128
  net = conv(net, name="conv2_1", kh=3, kw=3, n_out=128)
  net = conv(net, name="conv2_2", kh=3, kw=3, n_out=128)
  net = pool(net, name="pool2",   kh=2, kw=2, dh=2, dw=2)

  # # block 3 -- outputs 28x28x256
  net = conv(net, name="conv3_1", kh=3, kw=3, n_out=256)
  net = conv(net, name="conv3_2", kh=3, kw=3, n_out=256)
  net = pool(net, name="pool3",   kh=2, kw=2, dh=2, dw=2)

  # block 4 -- outputs 14x14x512
  net = conv(net, name="conv4_1", kh=3, kw=3, n_out=512)
  net = conv(net, name="conv4_2", kh=3, kw=3, n_out=512)
  net = conv(net, name="conv4_3", kh=3, kw=3, n_out=512)
  net = pool(net, name="pool4",   kh=2, kw=2, dh=2, dw=2)

  # block 5 -- outputs 7x7x512
  net = conv(net, name="conv5_1", kh=3, kw=3, n_out=512)
  net = conv(net, name="conv5_2", kh=3, kw=3, n_out=512)
  net = conv(net, name="conv5_3", kh=3, kw=3, n_out=512)
  net = pool(net, name="pool5",   kh=2, kw=2, dw=2, dh=2)

  # flatten
  flattened_shape = np.prod([s.value for s in net.get_shape()[1:]])
  net = tf.reshape(net, [-1, flattened_shape], name="flatten")

  # fully connected
  net = fully_connected(net, name="fc6", n_out=4096)
  net = tf.nn.dropout(net, keep_prob)
  net = fully_connected(net, name="fc7", n_out=1024)
  net = tf.nn.dropout(net, keep_prob)
  net = fully_connected(net, name="fc8", n_out=256)
  net = tf.nn.dropout(net, keep_prob)

  # Output layer - sigmoid
  fc9W = _variable_with_weight_decay('weights', [256, OutputNodes], stddev=0.01, wd=1.0)
  fc9_in = tf.matmul(net, fc9W)
  fc9 = tf.nn.sigmoid(dl.layer.createBatchNormalization(fc9_in))
  _activation_summary(fc9)

  print("fc9-Output shape: {}".format(fc9.shape))

  return fc9