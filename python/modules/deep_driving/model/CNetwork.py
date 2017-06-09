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
    dl.layer.setupLogger(self.log)

    Scope = "Network"

    with tf.variable_scope(Scope):
      self.log("Creating network Graph...")

      Input       = self._preprocessImage(Inputs['Image'])
      OutputNodes = len(Inputs['Labels'])
      Output = Input

      self.log(" * network Input-Shape: {}".format(Input.shape))


      # Fully Connected Layer - 1024
      Output = dl.layer.createFullyConnected(Input=Output, Size=1024, Func="ReLU", Name="FC_1")

      # Fully Connected Layer - 256
      Output = dl.layer.createFullyConnected(Input=Output, Size=256, Func="ReLU", Name="FC_2")

      # Output Layer - 14
      Output = dl.layer.createDense(Input=Output, Size=OutputNodes, Name="Dense_3")


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
      return Image