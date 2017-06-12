import deep_learning as dl
import numpy as np
import os
import re
import tensorflow as tf

class CReader(dl.data.CReader):
  def __init__(self, Settings, IsTraining):
    self._BatchesInQueue = 10
    self._ImageShape = [Settings['Data']['ImageHeight'], Settings['Data']['ImageWidth'], 3]
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

    if self._IsTraining:
      with tf.name_scope("TrainingReader"):
        TrainingFilenames     = self._getFilenames(Settings['Data']['TrainingPath'])
        TrainingFileQueue     = self._createFileQueue(TrainingFilenames, self._IsTraining)
        TrainingInputs        = self._buildRawReader(Settings, TrainingFileQueue)
        TrainingBatchedInputs = self._createBatch(TrainingInputs, self.getBatchSize(), self._IsTraining)

    with tf.name_scope("ValidationReader"):
      TestingFilenames     = self._getFilenames(Settings['Data']['ValidatingPath'])
      TestingFileQueue     = self._createFileQueue(TestingFilenames, self._IsTraining)
      TestingInputs        = self._buildRawReader(Settings, TestingFileQueue)
      TestingBatchedInputs = self._createBatch(TestingInputs, self.getBatchSize(), self._IsTraining)

    if self._IsTraining:
      BatchedInput = tf.cond(self._Outputs['IsTraining'], lambda: TrainingBatchedInputs, lambda: TestingBatchedInputs)

    else:
      BatchedInput = TestingBatchedInputs

    self._Outputs["Image"]  = BatchedInput[0]
    self._Outputs["Labels"] = BatchedInput[1]

    print("* Input-Image has shape {}".format(self._Outputs["Image"].shape))
    print("* Input-Label has shape {}".format(self._Outputs["Labels"]))

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
      LabelBytes  = 1
      ImageBytes  = np.prod(self._ImageShape)
      TotalBytes  = LabelBytes + ImageBytes

      Reader = tf.FixedLengthRecordReader(record_bytes=TotalBytes)
      _, Value = Reader.read(FileQueue)

      Record = tf.decode_raw(Value, tf.uint8)
      Labels = tf.squeeze(tf.cast(tf.slice(Record, [0], [LabelBytes]), tf.int32), name = "Label")
      RawImage = tf.reshape(tf.slice(Record, [LabelBytes], [ImageBytes]), [self._ImageShape[2], self._ImageShape[0], self._ImageShape[1]], name="RawImage")
      Images = tf.cast(tf.transpose(RawImage, [1, 2, 0]), tf.float32, name="Image")/255.0

    return [Images, Labels]


  def _getWeightDecayFactor(self):
    if "Optimizer" in self._Settings:
      if "WeightDecay" in self._Settings["Optimizer"]:
        return self._Settings["Optimizer"]["WeightDecay"]

    return 0


  _FilePattern = re.compile(".+.bin")
  def _getFilenames(self, Path):
    FileList = []

    for File in os.listdir(Path):
      if self._FilePattern.match(File):
        FileList.append(os.path.join(Path, File))

    return FileList