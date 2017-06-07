import deep_learning as dl
import numpy as np
import os
import re
import tensorflow as tf

from .. import db

class CReader(dl.data.CReader):
  def __init__(self, Settings, IsTraining):
    self._ImageShape = [32, 32, 3]
    self._Outputs = {
#      "Features": tf.placeholder(dtype=tf.float32, shape=[None, ] + self._ImageShape, name="Image"),
#      "Label": tf.placeholder(dtype=tf.int32, shape=[None, ], name="Label"),
      "Images":     None,
      "Labels":     None,
      "IsTraining": tf.placeholder(dtype=tf.bool, name="IsTraining"),
      "Lambda":     tf.placeholder(dtype=tf.float32, name="Lambda")
    }
    super().__init__(Settings, IsTraining)


  def _getOutputs(self, Inputs):
    return self._Outputs


  def _build(self, Settings):
    print("Build File-Reader Graph:")
    print("* Training is enabled: {}".format(self._IsTraining))

    with tf.name_scope("TrainingReader"):
      TrainingFilenames     = db.getDBFilenames(Settings['Data']['TrainingPath'])
      TrainingFileQueue     = self._createFileQueue(TrainingFilenames, self._IsTraining)
      TrainingInputs        = self._buildRawReader(Settings, TrainingFileQueue)
      TrainingBatchedInputs = self._createBatch(TrainingInputs, self.getBatchSize(), self._IsTraining)

    self._Outputs["Image"]  = TrainingBatchedInputs[0]
    self._Outputs["Labels"] = TrainingBatchedInputs[1:15]

    print("* Input-Image  has shape {}".format(self._Outputs["Image"].shape))
    for i, Output in enumerate(self._Outputs['Labels']):
      print("* Input-Label {} has shape {}".format(i, Output.shape))

    return TrainingBatchedInputs


  def _readBatch(self, Session, Inputs):
#    BatchList = list(Session.run(Inputs))

    return {
#      self._Outputs['Features']:   BatchList[0],
#      self._Outputs['Label']:      BatchList[1],
      self._Outputs['IsTraining']: self._IsTraining,
      self._Outputs['Lambda']:     self._getWeightDecayFactor()
    }


  def _getBatchSize(self, Settings):
    return Settings['Data']['BatchSize']


  def _addSummaries(self, Inputs):
    tf.summary.image('Images', Inputs[0])
    tf.summary.scalar('IsTraining', tf.cast(self._Outputs['IsTraining'], tf.uint8))


## Custom Methods

  def _buildRawReader(self, Settings, FileQueue):
    with tf.name_scope("FileReader"):
      Reader = tf.TFRecordReader()

      _, SerializedExample = Reader.read(FileQueue)
      Inputs = db.buildFeatureParser(SerializedExample)
      Inputs[0] = tf.image.resize_images(Inputs[0], size=(Settings['Data']['ImageHeight'], Settings['Data']['ImageWidth']))

    return Inputs


  def _getWeightDecayFactor(self):
    if "Optimizer" in self._Settings:
      if "WeightDecay" in self._Settings["Optimizer"]:
        return self._Settings["Optimizer"]["WeightDecay"]

    return 0
