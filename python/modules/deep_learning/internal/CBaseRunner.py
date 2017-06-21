import debug
import os
import time
import tensorflow as tf

from .. import checkpoint
from .. import printer
from .. import summary


class CBaseRunner():
  def __init__(self, Settings):
    self._Sesstion = None
    self._Saver = None
    self._EpochCount = 0
    self._SummaryDir = None
    self._LastCheckpointFile = "unknown"
    self._Network = None

    if Settings is None:
      self._Settings = {}
    else:
      self._Settings = Settings

    self._initBase()

  def _initBase(self):
    GPUFraction = self._getGPUFraction(self._Settings)
    if GPUFraction != None and GPUFraction > 0.0 and GPUFraction <= 1.0:
      print("Limit GPU memory usage to {}%".format(GPUFraction*100))
      GPUOptions = tf.GPUOptions(per_process_gpu_memory_fraction=GPUFraction)

    else:
      GPUOptions = tf.GPUOptions()

    self._Session = tf.Session(config=tf.ConfigProto(gpu_options=GPUOptions))
    self._Saver = None

  def reset(self, CheckpointDir):
    debug.Assert(self._Network != None, "There is no network defined for this Runner.")
    self._Saver = tf.train.Saver(max_to_keep=100)
    self._Network.initVariables(self._Session, CheckpointDir)
    self._EpochCount = 0
    self._LastCheckpointFile = "unknown"

    self._setSummaryDirAfterReset()


  def restore(self, CheckpointFile):
    self._Saver = tf.train.Saver(max_to_keep=100)
    if CheckpointFile == None:
      debug.logWarning("No checkpoint file given to restore from!")
      return 0

    self._EpochCount = checkpoint.getEpochNumberFromCheckpoint(CheckpointFile)
    print("Restore from Checkpoint {} with Epoch-Number {}".format(CheckpointFile, self._EpochCount))
    self._Saver.restore(self._Session, CheckpointFile)

    self._setSummaryDirAfterRestore()
    self._LastCheckpointFile = CheckpointFile

    return self._EpochCount


  def _setSummaryDirAfterReset(self):
    self._setNewSummaryDir()


  def _setSummaryDirAfterRestore(self):
    self._setOldSummaryDir()


  def _setNewSummaryDir(self):
    self._SummaryDir = None
    SummaryParentDir = self.getSummaryDir()
    if SummaryParentDir != None:
      self._SummaryDir = os.path.join(SummaryParentDir, summary.getNextSummaryDir(SummaryParentDir))


  def _setOldSummaryDir(self):
    self._SummaryDir = None
    SummaryParentDir = self.getSummaryDir()
    if SummaryParentDir != None:
      self._SummaryDir = os.path.join(SummaryParentDir, summary.getLastSummaryDir(SummaryParentDir))


  def addPrinter(self, Printer):
    debug.Assert(isinstance(Printer, printer.CPrinter))
    self._Printer = Printer

  def getPrinter(self):
    return self._Printer

  def addSummaryMerger(self, Merger):
    debug.Assert(isinstance(Merger, summary.CMerger))
    self._SummaryMerger = Merger

  def saveModel(self, CheckpointPath, Epoch = None):
    if Epoch == None:
      Epoch = self._EpochCount
    os.makedirs(CheckpointPath, exist_ok=True)
    CheckpointName = checkpoint.getCheckpointFilename(CheckpointPath, Epoch)
    saveCheckpointToFile(self._Saver, self._Session, CheckpointName, Tries = 5)


  def getSummaryDir(self):
    return self._getSummaryDir(self._Settings)


  def _printProgressBar(self, PrefixName, BarSize, Iteration, Epoch, Batch, IterationsPerEpoch):
    Percent = Batch/IterationsPerEpoch
    Bar = '.' * int((BarSize*Percent))
    BarString = str("{:<"+str(BarSize)+"}").format(Bar)

    Prefix = str("{} Epoch {}").format(PrefixName, Epoch)

    print("\r{:>8}: ({}) [{}] - {} / {}".format(Iteration, Prefix, BarString, Batch, IterationsPerEpoch), end='', flush=True)
    print("\r{:>8}: ({}) [{}] - {} / {}".format(Iteration, Prefix, BarString, Batch, IterationsPerEpoch), end='', flush=True)
    if Batch >= (IterationsPerEpoch-1):
      print("\r", end='', flush=True)


  def _getGPUFraction(self, Settings):
    if "Runner" in Settings:
      if "Memory" in Settings["Runner"]:
        return Settings["Runner"]["Memory"]

    return None

def saveCheckpointToFile(Saver, Session, Filename, Tries = 5):
  print("Store current model as checkpoint: {}".format(Filename))
  IsStored = False
  NumberOfTries = Tries
  while not IsStored:
    try:
      Saver.save(Session, Filename)
      IsStored = True
    except Error:
      if NumberOfTries <= 0:
        debug.logError("Cannot store checkpoint. I tried it several times...")
        raise Error

      else:
        debug.logWarning("Cannot store checkpoint, because the file is blocked. I'll try it again in 500ms...")
        NumberOfTries -= 1
        time.sleep(0.5)