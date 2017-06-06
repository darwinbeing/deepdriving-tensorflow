import re
import tensorflow as tf

from .CPrinter import CPrinter

class CProgressPrinter(CPrinter):
  def __init__(self, LossName = "Loss", ErrorName = "Error"):
    self._LossName  = LossName
    self._ErrorName = ErrorName
    self._MaxEpochs = None
    self._PreString = None
    super().__init__()


  def setupTraining(self, MaxEpochs):
    self._MaxEpochs = MaxEpochs
    self._PreString = "Training"


  def setupEvaluation(self, MaxEpochs):
    self._MaxEpochs = MaxEpochs
    self._PreString = "Evaluation"


  def _printEpochUpdate(self, SummaryDict):
    Loss  = self._getValueFromKey(SummaryDict, self._LossName)
    Error = self._getValueFromKey(SummaryDict, self._ErrorName)

    ProgressString = "{}: ".format(SummaryDict['Iteration'])
    if self._PreString != None:
      ProgressString += self._PreString + " "

    ProgressString += "Progress Epoch {}".format(SummaryDict['Epoch'])

    if self._MaxEpochs != None:
      ProgressString += "/{}".format(self._MaxEpochs)

    if Loss != None:
      ProgressString += " - Loss: {:.5f}".format(Loss)

    if Error != None:
      ProgressString += " Error: {:.2f}%".format(Error * 100)

    ProgressString += self._getTimingInformation(SummaryDict)
    print(ProgressString)

## Custom Methods
  def _getValueFromKey(self, Dict, KeyName):
    for Key in Dict.keys():
      if re.search(KeyName, Key):
        return Dict[Key]

    return None


  def _getTimingInformation(self, Dict):
    ProgressString = " ("
    ProgressString += "{:.3f} s/Epoch".format(Dict['Duration'])
    ProgressString += ", "

    if Dict['Duration'] > 0:
      SamplesPerSec = Dict['SampleCount']/Dict['Duration']
    else:
      SamplesPerSec = 0

    ProgressString += "{:.3f} Samples/s".format(SamplesPerSec)
    ProgressString += ")"
    return ProgressString
