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


class CAlexNet(dl.network.CNetwork):
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
      Output = Input

      Output = self._buildAlexNet(Output, OutputNodes)

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

  def _buildAlexNet(self, Input, OutputNodes):
    # This code and the weights are taken from: http://www.cs.toronto.edu/~guerzhoy/tf_alexnet/

    ################################################################################
    #
    # (self.feed('data')
    #         .conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
    #         .lrn(2, 2e-05, 0.75, name='norm1')
    #         .max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
    #         .conv(5, 5, 256, 1, 1, group=2, name='conv2')
    #         .lrn(2, 2e-05, 0.75, name='norm2')
    #         .max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
    #         .conv(3, 3, 384, 1, 1, name='conv3')
    #         .conv(3, 3, 384, 1, 1, group=2, name='conv4')
    #         .conv(3, 3, 256, 1, 1, group=2, name='conv5')
    #         .fc(4096, name='fc6')
    #         .fc(4096, name='fc7')
    #         .fc(1000, relu=False, name='fc8')
    #         .softmax(name='prob'))

    from .cifar.TutorialHelper import _variable_with_weight_decay, _variable_on_cpu, _activation_summary
    import numpy as np
    net_data = np.load(open("bvlc_alexnet.npy", "rb"), encoding="latin1").item()

    def conv(input, kernel, biases, k_h, k_w, c_o, s_h, s_w, padding="VALID", group=1):
      '''From https://github.com/ethereon/caffe-tensorflow
      '''
      c_i = input.get_shape()[-1]
      assert c_i % group == 0
      assert c_o % group == 0
      convolve = lambda i, k: tf.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)

      if group == 1:
        conv = convolve(input, kernel)
      else:
        input_groups = tf.split(input, group, 3)  # tf.split(3, group, input)
        kernel_groups = tf.split(kernel, group, 3)  # tf.split(3, group, kernel)
        output_groups = [convolve(i, k) for i, k in zip(input_groups, kernel_groups)]
        conv = tf.concat(output_groups, 3)  # tf.concat(3, output_groups)
      return tf.reshape(tf.nn.bias_add(conv, biases), [-1] + conv.get_shape().as_list()[1:])

    # conv1
    # conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
    with tf.variable_scope('conv1') as scope:
      k_h = 11
      k_w = 11
      c_o = 96
      s_h = 4
      s_w = 4
      conv1W = tf.Variable(net_data["conv1"][0])
      conv1b = tf.Variable(net_data["conv1"][1])
      conv1_in = conv(Input, conv1W, conv1b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=1)
      conv1 = tf.nn.relu(conv1_in)
      dl.helpers.saveFeatureMap(conv1, "Features")
      _activation_summary(conv1)

    # lrn1
    # lrn(2, 2e-05, 0.75, name='norm1')
    with tf.variable_scope('lrn1') as scope:
      radius = 2
      alpha = 2e-05
      beta = 0.75
      bias = 1.0
      lrn1 = tf.nn.local_response_normalization(conv1,
                                              depth_radius=radius,
                                              alpha=alpha,
                                              beta=beta,
                                              bias=bias)

    # maxpool1
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
    with tf.variable_scope('pool1') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'VALID'
      maxpool1 = tf.nn.max_pool(lrn1, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

    # conv2
    # conv(5, 5, 256, 1, 1, group=2, name='conv2')
    with tf.variable_scope('conv2') as scope:
      k_h = 5
      k_w = 5
      c_o = 256
      s_h = 1
      s_w = 1
      group = 2
      conv2W = tf.Variable(net_data["conv2"][0])
      conv2b = tf.Variable(net_data["conv2"][1])
      conv2_in = conv(maxpool1, conv2W, conv2b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv2 = tf.nn.relu(conv2_in)
      dl.helpers.saveFeatureMap(conv2, "Features")
      _activation_summary(conv2)

    # lrn2
    # lrn(2, 2e-05, 0.75, name='norm2')
    with tf.variable_scope('lrn2') as scope:
      radius = 2
      alpha = 2e-05
      beta = 0.75
      bias = 1.0
      lrn2 = tf.nn.local_response_normalization(conv2,
                                              depth_radius=radius,
                                              alpha=alpha,
                                              beta=beta,
                                              bias=bias)

    # maxpool2
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
    with tf.variable_scope('pool2') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'VALID'
      maxpool2 = tf.nn.max_pool(lrn2, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

    # conv3
    # conv(3, 3, 384, 1, 1, name='conv3')
    with tf.variable_scope('conv3') as scope:
      k_h = 3;
      k_w = 3;
      c_o = 384;
      s_h = 1;
      s_w = 1;
      group = 1
      conv3W = tf.Variable(net_data["conv3"][0])
      conv3b = tf.Variable(net_data["conv3"][1])
      conv3_in = conv(maxpool2, conv3W, conv3b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv3 = tf.nn.relu(conv3_in)
      dl.helpers.saveFeatureMap(conv3, "Features")
      _activation_summary(conv3)

    # conv4
    # conv(3, 3, 384, 1, 1, group=2, name='conv4')
    with tf.variable_scope('conv4') as scope:
      k_h = 3
      k_w = 3
      c_o = 384
      s_h = 1
      s_w = 1
      group = 2
      conv4W = tf.Variable(net_data["conv4"][0])
      conv4b = tf.Variable(net_data["conv4"][1])
      conv4_in = conv(conv3, conv4W, conv4b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv4 = tf.nn.relu(conv4_in)
      dl.helpers.saveFeatureMap(conv4, "Features")
      _activation_summary(conv4)

    # conv5
    # conv(3, 3, 256, 1, 1, group=2, name='conv5')
    with tf.variable_scope('conv5') as scope:
      k_h = 3
      k_w = 3
      c_o = 256
      s_h = 1
      s_w = 1
      group = 2
      conv5W = tf.Variable(net_data["conv5"][0])
      conv5b = tf.Variable(net_data["conv5"][1])
      conv5_in = conv(conv4, conv5W, conv5b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv5 = tf.nn.relu(conv5_in)
      dl.helpers.saveFeatureMap(conv5, "Features")
      _activation_summary(conv5)

    # maxpool5
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool5')
    with tf.variable_scope('pool5') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'VALID'
      maxpool5 = tf.nn.max_pool(conv5, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

    # fc6
    # fc(4096, name='fc6')
    with tf.variable_scope('fc6') as scope:
      Layer5Nodes = int(np.prod(maxpool5.get_shape()[1:]))
      layer5 = tf.reshape(maxpool5, [-1, Layer5Nodes])
      fc6W = _variable_with_weight_decay('weights6', shape=[Layer5Nodes, 4096],
                                          stddev=0.04, wd=1.0)
      fc6b = _variable_on_cpu('biase6', [4096], tf.constant_initializer(0.1))
      fc6 = tf.nn.relu_layer(layer5, fc6W, fc6b)
      _activation_summary(fc6)

    # fc7
    # fc(4096, name='fc7')
    with tf.variable_scope('fc7') as scope:
      fc7W = _variable_with_weight_decay('weights7', shape=[4096, 4096],
                                          stddev=0.04, wd=1.0)
      fc7b = _variable_on_cpu('biase7', [4096], tf.constant_initializer(0.1))
      fc7 = tf.nn.relu_layer(fc6, fc7W, fc7b)
      _activation_summary(fc7)

    # fc8
    # fc(256, name='fc8')
    with tf.variable_scope('fc8') as scope:
      fc8W = _variable_with_weight_decay('weights8', shape=[4096, 256],
                                          stddev=0.04, wd=1.0)
      fc8b = _variable_on_cpu('biase8', [256], tf.constant_initializer(0.1))
      fc8 = tf.nn.relu_layer(fc7, fc8W, fc8b)
      _activation_summary(fc8)

    # fc9(14, sigmoid)
    with tf.variable_scope('fc9') as scope:
      fc9W = _variable_with_weight_decay('weights9', shape=[256, OutputNodes],
                                          stddev=0.04, wd=1.0)
      fc9b = _variable_on_cpu('biases9', [OutputNodes], tf.constant_initializer(0.1))
      fc9 = tf.nn.sigmoid(tf.matmul(fc8, fc9W) + fc9b)
      _activation_summary(fc9)

    return fc9