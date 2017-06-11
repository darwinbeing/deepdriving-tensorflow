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


class CNetwork(dl.network.CNetwork):
  def _build(self, Inputs, Settings):
    dl.layer.Setup.setupLogger(self.log)
    dl.layer.Setup.setupIsTraining(Inputs['IsTraining'])
    dl.layer.Setup.setupHistogram(False)
    dl.layer.Setup.setupOutputText(True)
    dl.layer.Setup.setupFeatureMap(True)

    Scope = "Network"

    with tf.variable_scope(Scope):
      self.log("Creating network Graph...")

      Input       = self._preprocessImage(Inputs['Image'])
      OutputNodes = len(Inputs['Labels'])
      Output = Input

      self.log(" * network Input-Shape: {}".format(Input.shape))


      # Convolution layer
      with tf.name_scope("Layer_1"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=11, Filters=96, Stride=4, Name="Conv")
        Output = dl.layer.createBatchNormalization(Input=Output, Name="BN")
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        Output = dl.layer.createPooling(Input=Output, Size=3, Stride=2, Pool="MAX", Name="Pool")
        dl.helpers.saveFeatureMap(Output, "Features")
        #Output = dl.layer.createLRN(Input=Output, LocalSize=5, Alpha=0.0001, Beta=0.75, Name="LRN")

      # Convolution layer
      with tf.name_scope("Layer_2"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=5, Filters=256, Stride=1, Name="Conv")
        Output = dl.layer.createBatchNormalization(Input=Output, Name="BN")
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        Output = dl.layer.createPooling(Input=Output, Size=3, Stride=2, Pool="MAX", Name="Pool")
        dl.helpers.saveFeatureMap(Output, "Features")
        #Output = dl.layer.createLRN(Input=Output, LocalSize=5, Alpha=0.0001, Beta=0.75, Name="LRN")

      # Convolution layer
      with tf.name_scope("Layer_3"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=3, Filters=384, Stride=1, Name="Conv")
        Output = dl.layer.createBatchNormalization(Input=Output, Name="BN")
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        dl.helpers.saveFeatureMap(Output, "Features")

      # Convolution layer
      with tf.name_scope("Layer_4"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=3, Filters=384, Stride=1, Name="Conv")
        Output = dl.layer.createBatchNormalization(Input=Output, Name="BN")
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        dl.helpers.saveFeatureMap(Output, "Features")

      # Convolution layer
      with tf.name_scope("Layer_5"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=3, Filters=256, Stride=1, Name="Conv")
        Output = dl.layer.createBatchNormalization(Input=Output, Name="BN")
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        Output = dl.layer.createPooling(Input=Output, Size=3, Stride=2, Pool="MAX", Name="Pool")
        dl.helpers.saveFeatureMap(Output, "Features")

      # Fully Connected Layer
      with tf.name_scope("Layer_6"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=4096, Func="ReLU", Name="FC")
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Fully Connected Layer
      with tf.name_scope("Layer_7"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=4096, Func="ReLU", Name="FC")
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Fully Connected Layer
      with tf.name_scope("Layer_8"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=256, Func="ReLU", Name="FC")
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Output Layer
      with tf.name_scope("Output"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=OutputNodes, Func="Sigmoid", Name="FC")


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

#  def _createActivation(self, Signal, Activation = tf.identity, Name="Activation"):
#    with tf.name_scope(Name):
#      Y       = Activation(Signal, name="y")
#      return Y


#  def _createFullyConnectedLayer(self, Inputs, OutputSize, Name="FullyConnected"):
#    with tf.name_scope(Name):
#      Signal = self._createDenseLayer(Inputs, OutputSize, Name="Dense")
#      return self._createActivation(Signal, tf.nn.relu, Name="Activation")


  def _preprocessImage(self, Image, Name = "Preprocessing"):
    with tf.name_scope(Name):
      self.log("* Preprocess Image by adding -0.5")
      Image = Image - 0.5
      Image = dl.layer.createBatchNormalization(Input=Image)
      return Image