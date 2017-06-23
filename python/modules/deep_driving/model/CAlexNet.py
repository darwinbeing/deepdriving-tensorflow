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


from deep_learning.layer import LearningRates

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
    # This code has been taken from the caffe-2-tensorflow generator at
    # https://github.com/ethereon/caffe-tensorflow
    #
    ################################################################################
    #
    # (self.feed('data')
    #          .conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
    #          .max_pool(3, 3, 2, 2, name='pool1')
    #          .lrn(2, 1.99999994948e-05, 0.75, name='norm1')
    #          .conv(5, 5, 256, 1, 1, group=2, name='conv2')
    #          .max_pool(3, 3, 2, 2, padding=None, name='pool2')
    #          .lrn(2, 1.99999994948e-05, 0.75, name='norm2')
    #          .conv(3, 3, 384, 1, 1, name='conv3')
    #          .conv(3, 3, 384, 1, 1, group=2, name='conv4')
    #          .conv(3, 3, 256, 1, 1, group=2, name='conv5')
    #          .max_pool(3, 3, 2, 2, padding=None, name='pool5')
    #          .fc(4096, name='fc6')
    #          .fc(4096, name='fc7')
    #          .fc(256, name='fc8')
    #          .fc(14, name='fc9'))

    from .cifar.TutorialHelper import _variable_with_weight_decay, _variable_on_cpu, _activation_summary
    import numpy as np

    # net_data = np.load(open("deepdriving.npy", "rb"), encoding="latin1").item()

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

      if biases is not None:
        output = tf.nn.bias_add(conv, biases)
      else:
        output = conv

      return tf.reshape(output, [-1] + conv.get_shape().as_list()[1:])


    print("Input shape: {}".format(Input.shape))

    # conv1
    # conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
    with tf.variable_scope('conv1') as scope:
      k_h = 11
      k_w = 11
      c_o = 96
      s_h = 4
      s_w = 4

      conv1W = _variable_with_weight_decay('weights', [k_h, k_h, 3, c_o], stddev=0.01, wd=1.0)

      conv1_in = conv(Input, conv1W, None, k_h, k_w, c_o, s_h, s_w, padding="VALID", group=1)
      conv1 = tf.nn.relu(dl.layer.createBatchNormalization(conv1_in))
      dl.helpers.saveFeatureMap(conv1, "Features")
      _activation_summary(conv1)

      print("Conv1-Output shape: {}".format(conv1.shape))

    # maxpool1
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
    with tf.variable_scope('pool1') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'SAME'
      maxpool1 = tf.nn.max_pool(conv1, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

      print("Pool1-Output shape: {}".format(maxpool1.shape))


    # conv2
    # conv(5, 5, 256, 1, 1, group=2, name='conv2')
    with tf.variable_scope('conv2') as scope:
      k_h = 5
      k_w = 5
      c_o = 256
      s_h = 1
      s_w = 1
      group = 2

      conv2W = _variable_with_weight_decay('weights', [k_h, k_h, 48, c_o], stddev=0.01, wd=1.0)

      conv2_in = conv(maxpool1, conv2W, None, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv2 = tf.nn.relu(dl.layer.createBatchNormalization(conv2_in))
      dl.helpers.saveFeatureMap(conv2, "Features")
      _activation_summary(conv2)

      print("Conv2-Output shape: {}".format(conv2.shape))


    # maxpool2
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
    with tf.variable_scope('pool2') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'SAME'
      maxpool2 = tf.nn.max_pool(conv2, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

      print("Pool2-Output shape: {}".format(maxpool2.shape))


    # conv3
    # conv(3, 3, 384, 1, 1, name='conv3')
    with tf.variable_scope('conv3') as scope:
      k_h = 3;
      k_w = 3;
      c_o = 384;
      s_h = 1;
      s_w = 1;
      group = 1

      conv3W = _variable_with_weight_decay('weights', [k_h, k_h, 256, c_o], stddev=0.01, wd=1.0)

      conv3_in = conv(maxpool2, conv3W, None, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv3 = tf.nn.relu(dl.layer.createBatchNormalization(conv3_in))
      dl.helpers.saveFeatureMap(conv3, "Features")
      _activation_summary(conv3)

      print("Conv3-Output shape: {}".format(conv3.shape))


    # conv4
    # conv(3, 3, 384, 1, 1, group=2, name='conv4')
    with tf.variable_scope('conv4') as scope:
      k_h = 3
      k_w = 3
      c_o = 384
      s_h = 1
      s_w = 1
      group = 2

      conv4W = _variable_with_weight_decay('weights', [k_h, k_h, 192, c_o], stddev=0.01, wd=1.0)

      conv4_in = conv(conv3, conv4W, None, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv4 = tf.nn.relu(dl.layer.createBatchNormalization(conv4_in))
      dl.helpers.saveFeatureMap(conv4, "Features")
      _activation_summary(conv4)

      print("Conv4-Output shape: {}".format(conv4.shape))


    # conv5
    # conv(3, 3, 256, 1, 1, group=2, name='conv5')
    with tf.variable_scope('conv5') as scope:
      k_h = 3
      k_w = 3
      c_o = 256
      s_h = 1
      s_w = 1
      group = 2

      conv5W = _variable_with_weight_decay('weights', [k_h, k_h, 192, c_o], stddev=0.01, wd=1.0)

      conv5_in = conv(conv4, conv5W, None, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
      conv5 = tf.nn.relu(dl.layer.createBatchNormalization(conv5_in))
      dl.helpers.saveFeatureMap(conv5, "Features")
      _activation_summary(conv5)

      print("Conv5-Output shape: {}".format(conv5.shape))


    # maxpool5
    # max_pool(3, 3, 2, 2, padding='VALID', name='pool5')
    with tf.variable_scope('pool5') as scope:
      k_h = 3
      k_w = 3
      s_h = 2
      s_w = 2
      padding = 'VALID'
      maxpool5 = tf.nn.max_pool(conv5, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

      print("Pool5-Output shape: {}".format(maxpool5.shape))


    # fc6
    # fc(4096, name='fc6')
    with tf.variable_scope('fc6') as scope:
      Layer5Nodes = int(np.prod(maxpool5.get_shape()[1:]))
      layer5 = tf.reshape(maxpool5, [-1, Layer5Nodes])

      fc6W = _variable_with_weight_decay('weights', [Layer5Nodes, 4096], stddev=0.005, wd=1.0)

      fc6_in = tf.matmul(layer5, fc6W)
      fc6 = tf.nn.relu(dl.layer.createBatchNormalization(fc6_in))
      _activation_summary(fc6)

      print("fc6-Output shape: {}".format(fc6.shape))

      #fc6_drop = dl.layer.createDropout(Input=fc6, Ratio=0.5, Name="Drop")
      fc6_drop = fc6


    # fc7
    # fc(4096, name='fc7')
    with tf.variable_scope('fc7') as scope:
      fc7W = _variable_with_weight_decay('weights', [4096, 4096], stddev=0.005, wd=1.0)

      fc7_in = tf.matmul(fc6_drop, fc7W)
      fc7 = tf.nn.relu(dl.layer.createBatchNormalization(fc7_in))
      _activation_summary(fc7)

      print("fc7-Output shape: {}".format(fc7.shape))

      #fc7_drop = dl.layer.createDropout(Input=fc7, Ratio=0.5, Name="Drop")
      fc7_drop = fc7


    # fc8
    # fc(256, name='fc8')
    with tf.variable_scope('fc8') as scope:
      fc8W = _variable_with_weight_decay('weights', [4096, 256], stddev=0.01, wd=1.0)

      fc8_in = tf.matmul(fc7_drop, fc8W)
      fc8 = tf.nn.relu(dl.layer.createBatchNormalization(fc8_in))
      _activation_summary(fc8)

      print("fc8-Output shape: {}".format(fc8.shape))

      #fc8_drop = dl.layer.createDropout(Input=fc8, Ratio=0.5, Name="Drop")
      fc8_drop = fc8


    # fc9(14, sigmoid)
    with tf.variable_scope('fc9') as scope:
      fc9W = _variable_with_weight_decay('weights', [256, 14], stddev=0.01, wd=1.0)

      fc9_in = tf.matmul(fc8_drop, fc9W)
      fc9 = tf.nn.sigmoid(dl.layer.createBatchNormalization(fc9_in))
      _activation_summary(fc9)

      print("fc9-Output shape: {}".format(fc9.shape))


    return fc9