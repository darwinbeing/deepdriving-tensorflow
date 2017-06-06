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
    Scope = "Network"

    with tf.variable_scope(Scope):
      print("Creating network Graph...")

      Input = self._preprocessImage(Inputs['Image'])

      print(" * network Input-Shape: {}".format(Input.shape))

      Output = Input
      Output = self._createDenseLayer(Inputs=Output, OutputSize=Inputs['Labels'].shape[1], Name="Dense1")

      print(" * network Output-Shape: {}".format(Output.shape))

      Variables, Tensors = dl.helpers.getTrainableVariablesInScope(Scope)
      print("Finished to build network with {} trainable variables in {} tensors.".format(Variables, Tensors))

    Structure = {
      "Input":  Input,
      "Output": Output
    }
    return  Structure


  def _getOutputs(self, Structure):
    return {'Output': Structure['Output']}

## Custom methods

  def _createDenseLayer(self, Inputs, OutputSize, Name="Dense"):
    OutputSize = int(OutputSize)
    print(" * Create Dense-Layer \"{}\" with {} output-nodes.".format(Name, OutputSize))
    with tf.name_scope(Name):
      X       = tf.identity(Inputs, name="X")
      Weights = tf.Variable(initial_value=tf.random_normal(shape=[int(X.shape[1]), OutputSize], mean=0, stddev=0.1), name = "W")
      Bias    = tf.Variable(initial_value=tf.random_normal(shape=[OutputSize],                  mean=0, stddev=0.1), name = "b")
      Signal  = tf.add(tf.matmul(X, Weights), Bias, name="s")
      return Signal


  def _createActivation(self, Signal, Activation = tf.identity, Name="Activation"):
    with tf.name_scope(Name):
      Y       = Activation(Signal, name="y")
      return Y


  def _createFullyConnectedLayer(self, Inputs, OutputSize, Name="FullyConnected"):
    with tf.name_scope(Name):
      Signal = self._createDenseLayer(Inputs, OutputSize, Name="Dense")
      return self._createActivation(Signal, tf.nn.relu, Name="Activation")


  def _preprocessImage(self, Image, Name = "Preprocessing"):
    with tf.name_scope(Name):
      NormalizedImage = Image - 0.5
      X = self._reshapeImageToVector(NormalizedImage, Name="Features")
      return X


  def _reshapeImageToVector(self, Image, Name="Image"):
    VectorSize = int(np.prod(Image.shape[1:]))
    return tf.reshape(Image, shape=[-1, VectorSize], name=Name)
