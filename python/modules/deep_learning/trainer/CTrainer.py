import debug
import tensorflow as tf
import time
import os

from .. import data
from .. import error
from .. import helpers
from .. import internal
from .. import network
from .. import checkpoint
from .. import layer


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
    self._SummaryMerger    = None

    self._IsReady = False
    self._OptimizerStep = None

    self._prepare(self._Settings)


  def _prepare(self, Settings):
    if not self._IsReady:
      self._OptimizerStep = self._createOptimizer(self._ErrorMeasurement, Settings)

      Variables, Tensors = helpers.getTrainableVariables()
      print("Current Model has {} parameters in {} trainable tensors.".format(Variables, Tensors))

      self.reset(self.getCheckpointDir())
      self._Summary = tf.summary.merge_all()
      self._IsReady = True

  def train(self, NumberOfEpochs = None):
    Session = self._Session

    # Init Writer is necessary
    TrainWriter = None
    ValWriter   = None
    if self._SummaryDir != None:
      print("Store tensorboard summary at directory {}".format(self._SummaryDir))
      TrainWriter = tf.summary.FileWriter(os.path.join(self._SummaryDir, "train"))
      TrainWriter.add_graph(Session.graph)
      ValWriter   = tf.summary.FileWriter(os.path.join(self._SummaryDir, "val"))
      ValWriter.add_graph(Session.graph)
    else:
      print("Do not store any summary")

    # Store settings
    if not os.path.exists(self.getCheckpointDir()):
      os.makedirs(self.getCheckpointDir())
    Filename = os.path.join(self.getCheckpointDir(), "train.cfg")
    print("Store training settings in file {}".format(Filename))
    with open(Filename, "w") as File:
      File.write(str(self._Settings))

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

    Writer = TrainWriter
    if Epoch > 0:
      # Do not write to summary, since is has already been written by the training before
      Writer = None

    self._postEpochAction(Writer, SummaryResult, OtherResults, StartTime, Iteration, Epoch, BatchSize)
    SummaryResult = self._internalValidationStep(Session, Iteration, 0, Epoch)

    Writer = ValWriter
    if Epoch > 0:
      # Do not write to summary, since is has already been written by the training before
      Writer = None

    self._postValidationAction(Writer, SummaryResult, Iteration, Epoch, BatchSize)

    # Training Loop
    StartTime = time.time()
    for EpochNumber in range(MaxEpochs):
      Epoch = EpochNumber + self._EpochCount + 1
      SampleCount = 0
      for Batch in range(IterationsPerEpoch):
        Iteration += 1
        SampleCount += BatchSize
        self._printTrainingBar(20, Iteration, Epoch, Batch, IterationsPerEpoch, True)
        self._internalTrainStep(Session, Iteration, Batch, Epoch)

      SummaryResult, OtherResults = self._internalEvalStep(Session, Iteration, 0, Epoch)
      StartTime = self._postEpochAction(TrainWriter, SummaryResult, OtherResults, StartTime, Iteration, Epoch, SampleCount)
      SummaryResult = self._internalValidationStep(Session, Iteration, 0, Epoch)
      self._postValidationAction(ValWriter, SummaryResult, Iteration, Epoch, BatchSize)

      self._saveCheckpoint(Epoch, EpochNumber == MaxEpochs)

    self._EpochCount = Epoch

    # Stop queues
    QueueCoordinage.request_stop()
    QueueCoordinage.join()

    # Close writer
    if TrainWriter != None:
      TrainWriter.close()

    # Close writer
    if ValWriter != None:
      ValWriter.close()


  def _internalEvalStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._Summary]

    RawResults = list(self._trainIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))

    SummaryResult = RawResults[0]
    if len(RawResults) > 1:
      OtherResults = RawResults[1:]
    else:
      OtherResults = []

    return SummaryResult, OtherResults


  def _internalValidationStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._Summary]

    IsTraining = self._Reader.IsTraining
    self._Reader.IsTraining = False

    #print("Validate {} Iterations...".format(self.getValidationIterations(self._Settings)))
    IterationsPerStep = self.getValidationIterations(self._Settings)
    for i in range(IterationsPerStep):
      self._printTrainingBar(20, Iteration, Epoch, i, IterationsPerStep, False)
      RawResults = list(self._trainIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))
      SummaryResult = RawResults[0]

      if self._SummaryMerger != None:
        self._SummaryMerger.add(SummaryResult)

    self._Reader.IsTraining = IsTraining

    if self._SummaryMerger != None:
      SummaryResult = self._SummaryMerger.merge()

    return SummaryResult


  def _internalTrainStep(self, Session, Iteration, Batch, Epoch):
    RunTargets = [self._OptimizerStep]
    RawResults = list(self._trainIteration(Session, RunTargets, self._Reader, Iteration, Batch, Epoch))

    return RawResults


  def _postValidationAction(self, Writer, Summary, Iteration, Epoch, SampleCount):
    if (Summary != None) and (Writer != None):
      Writer.add_summary(Summary, Epoch)

    if self._Printer != None:
      self._Printer.printValidationUpdate(Summary, Iteration, Epoch, SampleCount)


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


  def restore(self, Epoch=None):
    if Epoch is None:
      CheckpointFile = checkpoint.getLatestCheckpointFile(self.getCheckpointDir())

    else:
      CheckpointFile = checkpoint.getCheckpointFilename(self.getCheckpointDir(), Epoch)

    debug.Assert(CheckpointFile != None, "Cannot find checkpoint file {}.".format(CheckpointFile))
    super().restore(CheckpointFile)


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
        return os.path.join(Settings['Trainer']['CheckpointPath'], "State_{}".format(self._Network.State))

    return None

  def _getEpochsUntilCheckpoint(self, Settings):
    # You can overrite this function to specify the number of epochs until a checkpoint is stored
    if 'Trainer' in Settings:
      if 'CheckpointEpochs' in Settings['Trainer']:
        return Settings['Trainer']['CheckpointEpochs']

    return None


  def getValidationIterations(self, Settings):
    # You can overrite this function to specify the number of epochs until a checkpoint is stored
    if 'Validation' in Settings:
      if 'Samples' in Settings['Validation']:
        return int(Settings['Validation']['Samples']/self._Reader.getBatchSize())

    return 1


  def _printTrainingBar(self, BarSize, Iteration, Epoch, Batch, IterationsPerEpoch, IsTraining=True):
    Percent = Batch/IterationsPerEpoch
    Bar = '.' * int((BarSize*Percent))
    BarString = str("{:<"+str(BarSize)+"}").format(Bar)

    if IsTraining:
      Prefix = str("Training Epoch {}").format(Epoch)
    else:
      Prefix = str("Validation Epoch {}").format(Epoch)

    print("\r{:>8}: ({}) [{}] - {} / {}".format(Iteration, Prefix, BarString, Batch, IterationsPerEpoch), end='', flush=True)
    print("\r{:>8}: ({}) [{}] - {} / {}".format(Iteration, Prefix, BarString, Batch, IterationsPerEpoch), end='', flush=True)
    if Batch >= (IterationsPerEpoch-1):
      print("\r", end='', flush=True)


  def _applyNoise(self, Gradients, GradientNoise):
    if GradientNoise is not None and GradientNoise > 0.0:
      NoiseLevel = GradientNoise / (tf.sqrt(tf.cast((CurrentOptimizationStep + 1), tf.float32)))
      NoisyGradients = []
      print("Apply noise to gradients (nu = {})...".format(GradientNoise))
      # Taken from: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/layers/python/layers/optimizers.py
      for Gradient, Variable in Gradients:
        if Gradient is not None:
          if isinstance(Gradient, tf.IndexedSlices):
            GradientShape = Gradient.dense_shape
          else:
            GradientShape = Gradient.get_shape()

          Noise = tf.truncated_normal(GradientShape) * NoiseLevel
          Gradient += Noise

        NoisyGradients.append((Gradient, Variable))

    else:
      NoiseLevel = 0
      NoisyGradients = Gradients

    tf.summary.scalar("NoiseLevel", NoiseLevel)
    return NoisyGradients


  def _applyIndiviualLearningRates(self, Gradients):
    print("Apply individual learning rate scales...")
    ScaledGradients = []
    for Gradient, Variable in Gradients:
      Scale = layer.LearningRates.get(Variable.name)
      if Scale != None:
        Gradient *= Scale
        print(" * \"{}\" has scale {}".format(Variable.name, Scale))

      ScaledGradients.append((Gradient, Variable))

    return ScaledGradients


  def _addSumGradientSummary(self, Gradients):
    Sum = 0.0
    for Gradient, Variable in Gradients:
      Sum += tf.norm(Gradient)

    tf.summary.scalar("GradientNorm", Sum)


  def _addSingleGradientSummary(self, Gradients):
    for Gradient, Variable in Gradients:
      tf.summary.scalar(Variable.name, tf.norm(Gradient))


  def _addGradientNoiseSummary(self, Gradients, NoisyGradients):
    for i, (Gradients, Variable) in enumerate(Gradients):
      tf.summary.scalar(Variable.name, tf.norm(NoisyGradients[i][0]) - tf.norm(Gradients))