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
      Output = Input

      self.log(" * network Input-Shape: {}".format(Input.shape))

      # Output Layer
      with tf.name_scope("Output"):
        OutputNodes = 10
        Output = dl.layer.createDense(Input=Output, Size=OutputNodes)


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

  def _preprocessImage(self, Image, Name = "Preprocessing"):
    with tf.name_scope(Name):
      #self.log("* Preprocess Image")
      #Image -= 0.5
      #Image = dl.layer.createBatchNormalization(Input=Image)
      return Image