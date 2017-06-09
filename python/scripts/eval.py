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

class CEvalSettings(misc.settings.CSettings):
  _Dict = {
  'Data': {
    'ValidatingPath': "../../../validation",
    'BatchSize': 256,
    'ImageWidth': 32,
    'ImageHeight': 24
  },
  'Evaluator': {
    'EpochSize': 10000,
    'NumberOfEpochs': 24,
    'CheckpointPath': 'Checkpoint',
  },
  }

SettingFile = "eval.cfg"

def main():
  Settings = CEvalSettings(SettingFile)

  Model = dl.CModel(model.CNetwork)

  Evaluator = Model.createEvaluator(model.CEvaluator, model.CReader, model.CError, Settings)
  Evaluator.addPrinter(model.CPrinter())
  Evaluator.addSummaryMerger(model.CMerger())

  Evaluator.restore(dl.checkpoint.getLatestCheckpointFile(Settings['Evaluator']['CheckpointPath']))
  #Evaluator.restore(dl.checkpoint.getCheckpointFilename(Settings['Evaluator']['CheckpointPath'], 36))

  Error = Evaluator.eval()
  print("Mean Absolute Error: {:.2f}".format(Error))

  Summary = Evaluator.getSummary()
  Evaluator.getPrinter().printFullSummary(Summary)
  Evaluator.storeResults('result.txt')

if __name__ == "__main__":
  main()