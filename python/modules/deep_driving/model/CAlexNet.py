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
import deep_learning.layer.initializer as init
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

    Input = Inputs['Image']
    OutputNodes = len(Inputs['Labels'])

    Seq = dl.layer.Sequence("Network")

    # Setup standard initializer
    Conv2D_BN_ReLU = dl.layer.Conv2D_BN_ReLU.setKernelInit(init.NormalInitializer(stddev=0.01))
    Dense_BN_ReLU  = dl.layer.Dense_BN_ReLU.setWeightInit(init.NormalInitializer(stddev=0.005))


    with Seq.addLayerName("Conv"):
      Seq.add(Conv2D_BN_ReLU(Kernel=11, Filters=96, Stride=4, Padding="VALID"))
      Seq.add(dl.layer.MaxPooling(Window=3, Stride=2))

    with Seq.addLayerName("Conv"):
      Seq.add(Conv2D_BN_ReLU(Kernel=5, Filters=256, Groups=2))
      Seq.add(dl.layer.MaxPooling(Window=3, Stride=2))

    with Seq.addLayerName("Conv"):
      Seq.add(Conv2D_BN_ReLU(Kernel=3, Filters=384, Groups=1))

    with Seq.addLayerName("Conv"):
      Seq.add(Conv2D_BN_ReLU(Kernel=3, Filters=384, Groups=2))

    with Seq.addLayerName("Conv"):
      Seq.add(Conv2D_BN_ReLU(Kernel=3, Filters=256, Groups=2))
      Seq.add(dl.layer.MaxPooling(Window=3, Stride=2, Padding="VALID"))

    with Seq.addLayerName("Dense"):
      Seq.add(Dense_BN_ReLU(4096))
      Seq.add(dl.layer.Dropout(0.5))

    with Seq.addLayerName("Dense"):
      Seq.add(Dense_BN_ReLU(4096))
      Seq.add(dl.layer.Dropout(0.5))

    with Seq.addLayerName("Dense"):
      Seq.add(Dense_BN_ReLU(256)
              .setWeightInit(init.NormalInitializer(stddev=0.01)))
      Seq.add(dl.layer.Dropout(0.5))

    with Seq.addLayerName("Output"):
      Seq.add(dl.layer.Dense(OutputNodes)
              .setWeightDecay(0.0)
              .setWeightInit(init.NormalInitializer(stddev=0.01)))
      Seq.add(dl.layer.activation.Sigmoid())


    Output = Seq.apply(Input)

    # We have 14 outputs, output 1 is the only probability output, the remaining are regression outputs
    Outputs = tf.split(Output, 14, axis=1)

    for i, O in enumerate(Outputs):
      self.log("* Output {} has shape {}".format(i, O.shape))

    Variables, Tensors = dl.helpers.getTrainableVariablesInScope()
    self.log("Finished to build network with {} trainable variables in {} tensors.".format(Variables, Tensors))

    Structure = {
      "Input":  Input,
      "Output": Outputs
    }
    return  Structure


  def _getOutputs(self, Structure):
    return {'Output': Structure['Output']}