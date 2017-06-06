import deep_learning as dl
import numpy as np
import os
import tensorflow as tf


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
    #Filenames = self._getFilenames(Settings, self._IsTraining)
    #FileQueue = self._createFileQueue(Filenames, self._IsTraining)
    #Inputs = self._buildRawReader(Settings, FileQueue)
    #BatchedInputs = self._createBatch(Inputs, self.getBatchSize(), self._IsTraining)

    BatchedInputs = [
      tf.constant(value=0.5, dtype=tf.float32, shape=[self.getBatchSize()] + self._ImageShape, name="ConstImage"),
      tf.constant(value=0,   dtype=tf.float32, shape=[self.getBatchSize()] + [10],             name="ConstLabel"),
    ]

    self._Outputs["Image"]  = BatchedInputs[0]
    self._Outputs["Labels"] = BatchedInputs[1]

    print("* Input-Image  has shape {}".format(self._Outputs["Image"].shape))
    print("* Input-Labels have shape {}".format(self._Outputs["Labels"].shape))

    return BatchedInputs


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

  def _getFilenames(self, Settings, IsTraining):
    if IsTraining:
      return self._getTrainingFilepaths(Settings['Data']['TrainingPath'])

    else:
      return self._getTestFilepaths(Settings['Data']['TestingPath'])


  def _getTrainingFilepaths(self, Directory):
    Filenames = []
    for i in range(1, 6):
      Filename = os.path.join(Directory, "data_batch_{}.bin".format(i))
      print("* Add file {}".format(Filename))
      Filenames.append(Filename)

    return Filenames


  def _getTestFilepaths(self, Directory):
    Filenames = []
    Filenames.append(os.path.join(Directory, "test_batch.bin"))

    return Filenames


  def _getWeightDecayFactor(self):
    if "Optimizer" in self._Settings:
      if "WeightDecay" in self._Settings["Optimizer"]:
        return self._Settings["Optimizer"]["WeightDecay"]

    return 0
