import tensorflow as tf

class CPrinter():
  def __init__(self):
    self._SummaryParser = tf.Summary()

  def printEpochUpdate(self, Summary, Iteration, Epoch, Duration, SampleCount):
    SummaryDict = {}
    if Summary != None:
      self._SummaryParser.ParseFromString(Summary)
      for Value in self._SummaryParser.value:
        SummaryDict[Value.tag] = Value.simple_value

    SummaryDict['Iteration'] = Iteration
    SummaryDict['Epoch'] = Epoch
    SummaryDict['Duration'] = Duration
    SummaryDict['SampleCount'] = SampleCount

    self._printEpochUpdate(SummaryDict)


  def printValidationUpdate(self, Summary, Iteration, Epoch, SampleCount):
    SummaryDict = {}
    if Summary != None:
      self._SummaryParser.ParseFromString(Summary)
      for Value in self._SummaryParser.value:
        SummaryDict[Value.tag] = Value.simple_value

    SummaryDict['Iteration'] = Iteration
    SummaryDict['Epoch'] = Epoch
    SummaryDict['SampleCount'] = SampleCount

    self._printValidationUpdate(SummaryDict)


  def printFullSummary(self, Summary):
    SummaryDict = {}
    if Summary != None:
      self._SummaryParser.ParseFromString(Summary)
      for Value in self._SummaryParser.value:
        SummaryDict[Value.tag] = Value.simple_value

      self._printFullSummaryDict(SummaryDict)


  def _printEpochUpdate(self, SummaryDict):
    # You can overwrite this method to print a better Summary
    print(SummaryDict)

  def _printValidationUpdate(self, SummaryDict):
    # You can overwrite this method to print a better Summary
    print(SummaryDict)

  def _printFullSummaryDict(self, SummaryDict):
    # You can overwrite this method to print a better Summary
    print(SummaryDict)

  def setupTraining(self, MaxEpochs):
    # You can overwrite this method, it is called from a Trainer before training
    pass

  def setupEvaluation(self, MaxEpochs):
    # You can overwrite this method, it is called from a Evaluator before evluation
    pass



