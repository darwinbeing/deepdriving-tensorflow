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
    dl.layer.Setup.setupStoreSparsity(True)

    Scope = "Network"

    with tf.variable_scope(Scope):
      self.log("Creating network Graph...")

      Input       = Inputs['Image']
      OutputNodes = len(Inputs['Labels'])
      Output = Input

      self.log(" * network Input-Shape: {}".format(Input.shape))

      # Convolution layer
      with tf.name_scope("Layer_1"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=11, Filters=96, Stride=4, Name="Conv", BiasLR=2.0, Padding="VALID")
        #Output = dl.layer.createBatchNormalization(Input=Output)
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        Output = dl.layer.createPooling(Input=Output, Size=3, Stride=2, Pool="MAX", Name="Pool", Padding="VALID")
        dl.helpers.saveFeatureMap(Output, "Features")
        Output = dl.layer.createLRN(Input=Output, LocalSize=5, Alpha=0.0001, Beta=0.75, Name="LRN")

      Groups = 2
      Outputs = dl.layer.createFeatureGroups(Input=Output, NumberOfGroups=Groups)

      # Convolution layer
      for i in range(Groups):
        with tf.name_scope("Layer_2_G_{}".format(i)):
          Outputs[i] = dl.layer.createConvolution2d(Input=Outputs[i], Size=5, Filters=256/Groups, Stride=1, Name="Conv", BiasLR=2.0, Padding=2)
          #Outputs[i] = dl.layer.createBatchNormalization(Input=Outputs[i])
          Outputs[i] = dl.layer.createActivation(Input=Outputs[i], Func="ReLU", Name="ReLU")
          Outputs[i] = dl.layer.createPooling(Input=Outputs[i], Size=3, Stride=2, Pool="MAX", Name="Pool", Padding="VALID")
          dl.helpers.saveFeatureMap(Outputs[i], "Features")
          Outputs[i] = tf.identity(Outputs[i])
          Outputs[i] = dl.layer.createLRN(Input=Outputs[i], LocalSize=5, Alpha=0.0001, Beta=0.75, Name="LRN")

      Output = dl.layer.mergeFeatureGroups(Outputs)

      # Convolution layer
      with tf.name_scope("Layer_3"):
        Output = dl.layer.createConvolution2d(Input=Output, Size=3, Filters=384, Stride=1, Name="Conv", BiasLR=2.0, Padding="SAME")
        #Output = dl.layer.createBatchNormalization(Input=Output)
        Output = dl.layer.createActivation(Input=Output, Func="ReLU", Name="ReLU")
        dl.helpers.saveFeatureMap(Output, "Features")

      Groups = 2
      Outputs = dl.layer.createFeatureGroups(Input=Output, NumberOfGroups=Groups)

      # Convolution layer
      for i in range(Groups):
        with tf.name_scope("Layer_4_G_{}".format(i)):
          Outputs[i] = dl.layer.createConvolution2d(Input=Outputs[i], Size=3, Filters=384/Groups, Stride=1, Name="Conv", BiasLR=2.0, Padding="SAME")
          #Outputs[i] = dl.layer.createBatchNormalization(Input=Outputs[i])
          Outputs[i] = dl.layer.createActivation(Input=Outputs[i], Func="ReLU", Name="ReLU")
          dl.helpers.saveFeatureMap(Outputs[i], "Features")
          Outputs[i] = tf.identity(Outputs[i])


      # Convolution layer
      for i in range(Groups):
        with tf.name_scope("Layer_5_G_{}".format(i)):
          Outputs[i] = dl.layer.createConvolution2d(Input=Outputs[i], Size=3, Filters=256/Groups, Stride=1, Name="Conv", BiasLR=2.0, Padding="SAME")
          #Outputs[i] = dl.layer.createBatchNormalization(Input=Outputs[i])
          Outputs[i] = dl.layer.createActivation(Input=Outputs[i], Func="ReLU", Name="ReLU")
          Outputs[i] = dl.layer.createPooling(Input=Outputs[i], Size=3, Stride=2, Pool="MAX", Name="Pool", Padding="VALID")
          dl.helpers.saveFeatureMap(Outputs[i], "Features")
          Outputs[i] = tf.identity(Outputs[i])


      Output = dl.layer.mergeFeatureGroups(Outputs)

      # Fully Connected Layer
      with tf.name_scope("Layer_6"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=4096, Func="ReLU", Name="FC", BiasLR=2.0)
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Fully Connected Layer
      with tf.name_scope("Layer_7"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=4096, Func="ReLU", Name="FC", BiasLR=2.0)
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Fully Connected Layer
      with tf.name_scope("Layer_8"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=256, Func="ReLU", Name="FC", BiasLR=2.0)
        Output = dl.layer.createDropout(Input=Output, Ratio=0.5, Name="Drop")

      # Output Layer
      with tf.name_scope("Output"):
        Output = dl.layer.createFullyConnected(Input=Output, Size=OutputNodes, Func="Sigmoid", Name="FC", BiasLR=2.0)


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

