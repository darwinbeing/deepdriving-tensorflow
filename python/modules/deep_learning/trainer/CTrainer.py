import debug
import tensorflow as tf
import time

from .. import data
from .. import error
from .. import helpers
from .. import internal
from .. import network


class CTrainer(internal.CBaseRunner):
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
    self._OptimizerStep = None

    self._prepare(self._Settings)


  def _prepare(self, Settings):
    if not self._IsReady:
      self._OptimizerStep = self._createOptimizer(self._ErrorMeasurement, Settings)

      Variables, Tensors = helpers.getTrainableVariables()
      print("Current Model has {} parameters in {} trainable tensors.".format(Variables, Tensors))

      self.reset()
      self._Summary = tf.summary.merge_all()
      self._IsReady = True

  def train(self, NumberOfEpochs = None):
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
    MaxEpochs = self.getMaxEpochs() - self._EpochCount
    if NumberOfEpochs != None:
      MaxEpochs = min([NumberOfEpochs, MaxEpochs])

    # Setup Printer
    if self._Printer != None:
      self._Printer.setupTraining(self.getMaxEpochs())

    # Loop Preparation
    BatchSize = self._Reader.getBatchSize()
    Epoch = self._EpochCount
    IterationsPerEpoch = helpers.getIterationsPerEpoch(self.getEpochSize(), BatchSize)
    Iteration = Epoch * IterationsPerEpoch
    print("Run training for {} epochs beginning with epoch {} and {} iterations per epoch.".format(MaxEpochs, self._EpochCount, IterationsPerEpoch))

    # Initial Eval Step
    StartTime = time.time()
    SummaryResult, OtherResults = self._internalEvalStep(Session, Iteration, 0, Epoch)
    self._postEpochAction(Writer, SummaryResult, OtherResults, StartTime, Iteration, Epoch, BatchSize)

    # Training Loop
    StartTime = time.time()
    for EpochNumber in range(MaxEpochs):
      Epoch = EpochNumber + self._EpochCount + 1
      SampleCount = 0
      for Batch in range(IterationsPerEpoch):
        Iteration += 1
        SampleCount += BatchSize
        SummaryResult, OtherResults = self._internalTrainStep(Session, Iteration, Batch, Epoch)

      StartTime = self._postEpochAction(Writer, SummaryResult, OtherResults, StartTime, Iteration, Epoch, SampleCount)
      self._saveCheckpoint(Epoch, EpochNumber == MaxEpochs)

    self._EpochCount = Epoch

    # Stop queues
    QueueCoordinage.request_stop()
    QueueCoordinage.join()

    # Close writer
    if Writer != None:
      Writer.close()


  def _internalEvalStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._Summary]
    RawResults = list(self._trainIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))
    SummaryResult = RawResults[0]
    if len(RawResults) > 1:
      OtherResults = RawResults[1:]
    else:
      OtherResults = []

    return SummaryResult, OtherResults


  def _internalTrainStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._OptimizerStep, self._Summary]
    RawResults = list(self._trainIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))
    SummaryResult = RawResults[1]
    if len(RawResults) > 1:
      OtherResults = RawResults[2:]
    else:
      OtherResults = []

    return SummaryResult, OtherResults


  def _postEpochAction(self, Writer, Summary, OtherResults, StartTime, Iteration, Epoch, SampleCount):
    Duration = (time.time() - StartTime)
    StartTime = time.time()

    if (Summary != None) and (Writer != None):
      Writer.add_summary(Summary, Epoch)

    if self._Printer != None:
      self._Printer.printEpochUpdate(Summary, Iteration, Epoch, Duration, SampleCount)

    return StartTime


  def _saveCheckpoint(self, Epoch, IsForceSave = False):
    EpochsUntilCheckpoint = self.getEpochsUntilCheckpoint()
    IsSave = False
    if EpochsUntilCheckpoint != None:
      if Epoch %  EpochsUntilCheckpoint == 0:
        IsSave = True

    if IsSave or IsForceSave:
      self.saveModel(self.getCheckpointDir(), Epoch)


  def getMaxEpochs(self):
    return self._getMaxEpochs(self._Settings)

  def getEpochSize(self):
    return self._getEpochSize(self._Settings)

  def getCheckpointDir(self):
    return self._getCheckpointDir(self._Settings)

  def getEpochsUntilCheckpoint(self):
    return self._getEpochsUntilCheckpoint(self._Settings)


  def _trainIteration(self, Session, RunTargets, Reader, Iteration, Batch, Epoch):
    raise Exception("You have to overwride this method and run a training iteration inside.")
    # Return the results here
    return None, None

  def _createOptimizer(self, ErrorMeasurement, Settings):
    raise Exception("You have to overwride this method and create an optimizer step to return.")
    return None

  def _getMaxEpochs(self, Settings):
    # You have to overwride this method to return the maximum number of epochs.
    return Settings['Trainer']['NumberOfEpochs']

  def _getEpochSize(self, Settings):
    # You have to overwride this method to return the epoch size.
    return Settings['Trainer']['EpochSize']

  def _getSummaryDir(self, Settings):
    # You can overrite this function to specify a summary directory
    if 'Trainer' in Settings:
      if 'SummaryPath' in Settings['Trainer']:
        return Settings['Trainer']['SummaryPath']

    return None

  def _getCheckpointDir(self, Settings):
    # You can overrite this function to specify a checkpoint directory
    if 'Trainer' in Settings:
      if 'CheckpointPath' in Settings['Trainer']:
        return Settings['Trainer']['CheckpointPath']

    return None

  def _getEpochsUntilCheckpoint(self, Settings):
    # You can overrite this function to specify the number of epochs until a checkpoint is stored
    if 'Trainer' in Settings:
      if 'CheckpointEpochs' in Settings['Trainer']:
        return Settings['Trainer']['CheckpointEpochs']

    return None