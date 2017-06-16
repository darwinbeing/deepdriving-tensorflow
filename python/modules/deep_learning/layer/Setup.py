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

from .. import helpers

class CSetup():
  def __init__(self):
    self._Log = self.logDefault
    self._IsTraining = None
    self._StoreHistogram = True
    self._StoreOutputAsText = True
    self._StoreSparsity = True
    self._Initializer = {
      'Weights': helpers.XavierInitializer(),
      'Bias': helpers.ConstantInitializer(0),
      'Kernel2D': helpers.XavierInitializerConv()
    }

  def logDefault(self, Text):
    print(Text)


  def setupLogger(self, Logger):
    self._Log = Logger


  def setupIsTraining(self, IsTraining):
    self._IsTraining = IsTraining


  def setupHistogram(self, IsEnabled):
    self._StoreHistogram = IsEnabled
    if self._StoreHistogram:
      print("* Store Histogram of Weights, Bias, Signal and Activation")
    else:
      print("* Do not store Histograms")


  def setupOutputText(self, IsEnabled):
    self._StoreOutputAsText = IsEnabled
    if self._StoreOutputAsText:
      print("* Store Output as Text")
    else:
      print("* Do not store Output as Text")


  def setupFeatureMap(self, IsEnabled):
    self._StoreFeatureMap = IsEnabled
    if self._StoreFeatureMap:
      print("* Store Feature Maps")
    else:
      print("* Do not store Feature Maps")


  def setupStoreSparsity(self, IsEnabled):
    self._StoreSparsity = IsEnabled
    if self._StoreSparsity:
      print("* Store the sparsity of parameters")
    else:
      print("* Do not store the sparsity of parameters")


  def setupKernelInitializer(self, Initializer):
    self._Initializer["Kernel2D"] = Initializer

  def setupWeightInitializer(self, Initializer):
    self._Initializer["Weights"] = Initializer

  def setupBiasInitializer(self, Initializer):
    self._Initializer["Bias"] = Initializer

  @property
  def StoreSparsity(self):
    return self._StoreSparsity

  @property
  def StoreFeatureMap(self):
    return self._StoreFeatureMap

  @property
  def StoreHistogram(self):
    return self._StoreHistogram

  @property
  def StoreOutputAsText(self):
    return self._StoreOutputAsText and helpers.checkVersion(1, 2)

  @property
  def Log(self):
    return self._Log

  @property
  def IsTraining(self):
    return self._IsTraining

  @property
  def Initializer(self):
    return self._Initializer

Setup = CSetup()