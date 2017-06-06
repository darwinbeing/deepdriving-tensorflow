import debug
import tensorflow as tf
import time

from .. import data
from .. import error
from .. import helpers
from .. import internal
from .. import network


class CEvaluator(internal.CBaseRunner):
  def __init__(self, Network, Reader, ErrorMeasurement, Settings = None):
    super().__init__(Settings)
    debug.Assert(isinstance(Network, network.CNetwork), "You must specify a Network object.")
    debug.Assert(isinstance(Reader, data.CReader), "You must specify a Reader object.")
    debug.Assert(isinstance(ErrorMeasurement, error.CMeasurement), "You must specify an ErrorMeasurement object.")

    self._Network          = Network
    self._Reader           = Reader
    self._ErrorMeasurement = ErrorMeasurement
    self._Printer          = None

    self._IsReady = False

    self._prepare(self._Settings)


  def _prepare(self, Settings):
    if not self._IsReady:
      Variables, Tensors = helpers.getTrainableVariables()
      print("Current Model has {} parameters in {} trainable tensors.".format(Variables, Tensors))

      self.reset()
      self._Summary = tf.summary.merge_all()
      self._IsReady = True


  def eval(self):
    Session = self._Session

    # Init Writer is necessary
    Writer = None
    if self._SummaryDir != None:
      print("Store tensorboard summary at directory {}".format(self._SummaryDir))
      Writer = tf.summary.FileWriter(self._SummaryDir, Session.graph)
    else:
      print("Do not store any summary")

    # Start queues
    QueueCoordinage = tf.train.Coordinator()
    tf.train.start_queue_runners(sess=Session, coord=QueueCoordinage)

    # Calculate number of epochs to run
    MaxEpochs = self.getMaxEpochs()

    # Setup Printer
    if self._Printer != None:
      self._Printer.setupEvaluation(self.getMaxEpochs())

    # Loop Preparation
    BatchSize = self._Reader.getBatchSize()
    Epoch = 0
    IterationsPerEpoch = helpers.getIterationsPerEpoch(self.getEpochSize(), BatchSize)
    Iteration = Epoch * IterationsPerEpoch
    ErrorSum = 0
    print("Run training for {} epochs beginning with epoch {} and {} iterations per epoch.".format(MaxEpochs, self._EpochCount, IterationsPerEpoch))

    # Evaluation Loop
    StartTime = time.time()
    for EpochNumber in range(MaxEpochs):
      Epoch = EpochNumber + 1
      SampleCount = 0
      for Batch in range(IterationsPerEpoch):
        Iteration += 1
        SampleCount += BatchSize
        SummaryResult, Error, OtherResults = self._internalEvalStep(Session, Iteration, Batch, Epoch)
        ErrorSum += Error

      StartTime = self._postEpochAction(Writer, SummaryResult, OtherResults, StartTime, Iteration, Epoch, SampleCount)

    # Stop queues
    QueueCoordinage.request_stop()
    QueueCoordinage.join()

    # Close writer
    if Writer != None:
      Writer.close()

    return ErrorSum/Iteration


  def _internalEvalStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._Summary, self._ErrorMeasurement.getEvalError()]
    RawResults = list(self._evalIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))
    SummaryResult = RawResults[0]
    Error = RawResults[1]
    if len(RawResults) > 2:
      OtherResults = RawResults[2:]
    else:
      OtherResults = []

    return SummaryResult, Error, OtherResults


  def _postEpochAction(self, Writer, Summary, OtherResults, StartTime, Iteration, Epoch, SampleCount):
    Duration = (time.time() - StartTime)
    StartTime = time.time()

    if (Summary != None) and (Writer != None):
      Writer.add_summary(Summary, Epoch)

    if self._Printer != None:
      self._Printer.printEpochUpdate(Summary, Iteration, Epoch, Duration, SampleCount)

    return StartTime


  def getMaxEpochs(self):
    return self._getMaxEpochs(self._Settings)


  def getEpochSize(self):
    return self._getEpochSize(self._Settings)


  def _trainIteration(self, Session, RunTargets, Reader, Iteration, Batch, Epoch):
    raise Exception("You have to overwride this method and run a eval iteration inside.")
    # Return the results here
    return None, None, None


  def _getMaxEpochs(self, Settings):
    # You have to overwride this method to return the maximum number of epochs.
    return Settings['Evaluator']['NumberOfEpochs']

  def _getEpochSize(self, Settings):
    # You have to overwride this method to return the epoch size.
    return Settings['Evaluator']['EpochSize']

  def _getSummaryDir(self, Settings):
    # You can overrite this function to specify a summary directory
    if 'Evaluator' in Settings:
      if 'SummaryPath' in Settings['Evaluator']:
        return Settings['Evaluator']['SummaryPath']

    return None


  def _setSummaryDirAfterRestore(self):
    self._setNewSummaryDir()