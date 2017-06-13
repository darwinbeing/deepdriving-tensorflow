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

import misc.settings
import deep_learning as dl
import deep_driving.model as model
import deep_driving.model.cifar as cifar

class CCalcSettings(misc.settings.CSettings):
  _Dict = {
  'Data': {
    'TrainingPath': "C:/Data/Cifar-10/training",
    'ValidatingPath': "C:/Data/Cifar-10/training",
    'BatchSize': 1,
    'ImageWidth': 32,
    'ImageHeight': 32
  },
  'MeanCalculator': {
    'EpochSize': 1,
    'NumberOfEpochs': 1,
    'MeanFile': 'image-mean',
  },
  }

SettingFile = "calc_mean.cfg"

def main():
  Settings = CCalcSettings(SettingFile)

  Calculator = dl.calculator.CMeanCalculator(cifar.CReader, Settings)

  Calculator.calculate()
  Calculator.store()


if __name__ == "__main__":
  main()