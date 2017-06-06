import os
import re

CheckpointFileName = "model_{}.ckpt"
CheckpointFilePattern = re.compile("model_(\d+).ckpt")
LatestCheckpointPattern = re.compile("model_checkpoint_path: \"(.+)\"")

def getLatestCheckpointFile(CheckpointDir):
  Epoch = getHighestCheckpointEpoch(CheckpointDir)

  if Epoch > 0:
    return os.path.join(CheckpointDir, CheckpointFileName.format(Epoch))

  else:
    return None

def getHighestCheckpointEpoch(CheckpointDir):
  CheckpointFile = os.path.join(CheckpointDir, "checkpoint")
  if not os.path.exists(CheckpointFile):
    return 0

  with open(CheckpointFile, "r") as File:
    HighestEpochNumber = 0
    for Line in File:
      if LatestCheckpointPattern.match(Line):
        LatestFile = LatestCheckpointPattern.search(Line).group(1)
        HighestEpochNumber = getEpochNumberFromCheckpoint(LatestFile)
        break

    File.close()

  return HighestEpochNumber

def getCheckpointFilename(CheckpointDir, Epoch):
  return os.path.join(CheckpointDir, CheckpointFileName.format(Epoch))

def getEpochNumberFromCheckpoint(CheckpointFile):
  return int(CheckpointFilePattern.search(CheckpointFile).group(1))