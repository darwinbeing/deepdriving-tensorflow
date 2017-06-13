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

import time

import misc.settings
import deep_learning as dl
import deep_driving.model as model
import deep_driving.model.cifar as cifar

class CTrainSettings(misc.settings.CSettings):
  _Dict = {
  'Data': {
    'TrainingPath':   "C:/Data/Cifar-10/training",
    'ValidatingPath': "C:/Data/Cifar-10/validation",
    'BatchSize': 1,
    'ImageWidth': 32,
    'ImageHeight': 32
  },
  'Trainer': {
    'EpochSize':        50000,
    'NumberOfEpochs':   50,
    'SummaryPath':      'Summary',
    'CheckpointPath':   'Checkpoint',
    'CheckpointEpochs': 10,
  },
  'Optimizer':{
    'StartingLearningRate': 0.005,
    'EpochsPerDecay':       10,
    'LearnRateDecay':       0.95,
    'WeightDecay':          0.004
  },
  'Validation': {
    'Samples': 10000
  },
  'PreProcessing':
  {
    'MeanFile': 'image-mean.tfrecord'
  },
  }

SettingFile = "train.cfg"
IsRetrain = True

def main():
  Settings = CTrainSettings(SettingFile)
  dl.summary.cleanSummary(Settings['Trainer']['SummaryPath'], 3)

  Model = dl.CModel(cifar.CNetwork)

  Trainer = Model.createTrainer(model.CTrainer, cifar.CReader, cifar.CError, Settings)
  Trainer.addPrinter(dl.printer.CProgressPrinter(LossName="Loss/Loss", ErrorName="ClassError/Error"))
  Trainer.addSummaryMerger(cifar.CMerger())

  if not IsRetrain:
    Trainer.restore()
    #Trainer.restore(3)

  StartTime = time.time()
  Trainer.train()
  DeltaTime = time.time() - StartTime
  print("Training took {}s ({})".format(DeltaTime, misc.time.getStringFromTime(DeltaTime)))

if __name__ == "__main__":
  main()