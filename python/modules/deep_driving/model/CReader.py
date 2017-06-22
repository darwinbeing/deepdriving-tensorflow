import deep_learning as dl
import numpy as np
import os
import re
import tensorflow as tf

from .. import db

class CReader(dl.data.CReader):
  def __init__(self, Settings, IsTraining, UsePreprocessing, ForceDataAugmentation):
    self._BatchesInQueue = 30
    self._ImageShape = [Settings['Data']['ImageHeight'], Settings['Data']['ImageWidth'], 3]
    self._Outputs = {
#      "Features": tf.placeholder(dtype=tf.float32, shape=[None, ] + self._ImageShape, name="Image"),
#      "Label": tf.placeholder(dtype=tf.int32, shape=[None, ], name="Label"),
      "Images":     None,
      "Labels":     None,
      "IsTraining": tf.placeholder(dtype=tf.bool, name="IsTraining"),
      "Lambda":     tf.placeholder(dtype=tf.float32, name="Lambda")
    }
    super().__init__(Settings, IsTraining, UsePreprocessing, ForceDataAugmentation)


  def _getOutputs(self, Inputs):
    return self._Outputs


  def _build(self, Settings):
    print("Build File-Reader Graph:")
    print("* Training is enabled: {}".format(self._IsTraining))

    if self._IsTraining:
      with tf.name_scope("TrainingReader"):
        TrainingFilenames     = db.getDBFilenames(Settings['Data']['TrainingPath'])
        TrainingFileQueue     = self._createFileQueue(TrainingFilenames, self._IsTraining)
        TrainingInputs        = self._buildRawReader(Settings, TrainingFileQueue)
        TrainingPreprocInputs = self._buildPreprocessing(Settings, TrainingInputs, self._IsTraining)
        TrainingBatchedInputs = self._createBatch(TrainingPreprocInputs, self.getBatchSize(), self._IsTraining)

    with tf.name_scope("ValidationReader"):
      TestingFilenames     = db.getDBFilenames(Settings['Data']['ValidatingPath'])
      TestingFileQueue     = self._createFileQueue(TestingFilenames, self._IsTraining)
      TestingInputs        = self._buildRawReader(Settings, TestingFileQueue)
      TestingPreprocInputs = self._buildPreprocessing(Settings, TestingInputs, False)
      TestingBatchedInputs = self._createBatch(TestingPreprocInputs, self.getBatchSize(), self._IsTraining)

    if self._IsTraining:
      BatchedInput = tf.cond(self._Outputs['IsTraining'], lambda: TrainingBatchedInputs, lambda: TestingBatchedInputs)

    else:
      BatchedInput = TestingBatchedInputs

    self._Outputs["Image"]  = BatchedInput[0]
    self._Outputs["Labels"] = BatchedInput[1:15]

    print("* Input-Image  has shape {}".format(self._Outputs["Image"].shape))
    for i, Output in enumerate(self._Outputs['Labels']):
      print("* Input-Label {} has shape {}".format(i, Output.shape))

    return BatchedInput


  def _readBatch(self, Session, Inputs):
#    BatchList = list(Session.run(Inputs))

    #print("Training: {}".format(self._IsTraining))

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
      Inputs[0] = tf.image.resize_images(Inputs[0], size=(self._ImageShape[0], self._ImageShape[1]))

    return Inputs

  def _buildPreprocessing(self, Settings, Inputs, UseDataAugmentation):
    Image = Inputs[0]

    if self._ForceDataAugmentation or UseDataAugmentation:
      with tf.name_scope("DataAugmentation"):

        #print("* Perform data-augmentation")

        #Image = tf.image.random_brightness(Image, max_delta=0.10)
        #Image = tf.image.random_contrast(Image, lower=0.90, upper=1.10)
        #Image = tf.image.random_saturation(Image, lower=0.90, upper=1.10)
        #Image = tf.image.random_hue(Image, max_delta=0.05)
        pass

    if self._UsePreprocessing:
      with tf.name_scope("Preprocessing"):

        print("* Perform per-pixel normalization")

        MeanReader = dl.data.CMeanReader()
        MeanReader.read(Settings['PreProcessing']['MeanFile'])

        MeanImage = tf.image.resize_images(MeanReader.MeanImage, size=(int(Image.shape[0]), int(Image.shape[1])))
        Image = tf.subtract(Image, MeanImage)

    Inputs[0] = Image
    return Inputs

  def _getWeightDecayFactor(self):
    if "Optimizer" in self._Settings:
      if "WeightDecay" in self._Settings["Optimizer"]:
        return self._Settings["Optimizer"]["WeightDecay"]

    return 0
