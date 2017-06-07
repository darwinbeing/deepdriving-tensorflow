import tensorflow as tf

from .. import helpers


class CReader():
  def __init__(self, Settings = None, IsTraining = False):
    self._IsReady =  False
    self._Inputs = []
    self._IsTraining = IsTraining
    if Settings != None:
      self._Settings = Settings
    else:
      self._Settings = {}

    self._PreprocessThreads = 8
    self._MinimumSamplesInQueue = 500

    self._prepare()

  def _prepare(self):
    if not self._IsReady:
      self._Inputs = self._build(self._Settings)
      self._addSummaries(self._Inputs)
      self._IsReady = True


  @property
  def IsTraining(self):
    return self._IsTraining

  @IsTraining.setter
  def IsTraining(self, Value):
    self._IsTraining = Value

  def _build(self, Settings):
    raise Exception("You must override this function to build a reader graph!")
    pass

  def _getOutputs(self, Inputs):
    raise Exception("You must override this function to deliver output placeholders or output tensors for the network!")
    return {}

  def _readBatch(self, Session, Inputs):
    raise Exception("You must override this function to read a batch!")
    return {}

  def _getBatchSize(self, Settings):
    raise Exception("You must override this function output the batchsize!")
    return {}

  def _addSummaries(self, Inputs):
    # You can overrite this function to add the inputs to the summary
    pass


  def _createBatch(self, Inputs, BatchSize, IsShuffle):
    #ReshapedBatchedInputs = []
    #for i, Input in enumerate(Inputs):
    #  InputShape = [BatchSize] + helpers.getShapeList(Input.shape)
    #  print("* Prepare Input Batch with Shape {}".format(InputShape))
    #  ReshapedBatchedInputs.append(tf.reshape(Input, shape=InputShape))
    #return ReshapedBatchedInputs

    with tf.name_scope("BatchGen"):
      print("* Generate Input Batches...")
      print("* With Batch-Size: {}".format(BatchSize))

      if not IsShuffle:
        print("* Do not shuffle Data for Batching...")
        BatchedInputs = list(tf.train.batch(
          Inputs,
          batch_size=BatchSize,
          num_threads=self._PreprocessThreads,
          capacity=self._MinimumSamplesInQueue + 3 * BatchSize))

      else:
        print("* Shuffle Data for Batching...")
        BatchedInputs = list(tf.train.shuffle_batch(
          Inputs,
          batch_size=BatchSize,
          num_threads=self._PreprocessThreads,
          capacity=self._MinimumSamplesInQueue + 3 * BatchSize,
          min_after_dequeue=self._MinimumSamplesInQueue))

      ReshapedBatchedInputs = []
      for i, Input in enumerate(Inputs):
        InputShape = [BatchSize] + helpers.getShapeList(Input.shape)
        print("* Prepare Input Batch with Shape {}".format(InputShape))
        ReshapedBatchedInputs.append(tf.reshape(BatchedInputs[i], shape=InputShape))

      return ReshapedBatchedInputs


  def _createFileQueue(self, Filenames, Shuffle = False):
    with tf.name_scope("FileQueue"):
      for File in Filenames:
        if not tf.gfile.Exists(File):
          raise ValueError('Failed to find file: ' + File)

      print("* Create File Queue with {} files.".format(len(Filenames)))
      return tf.train.string_input_producer(Filenames, capacity=4096, shuffle=Shuffle)

  def getOutputs(self):
    return self._getOutputs(self._Inputs)

  def readBatch(self, Session):
    return self._readBatch(Session, self._Inputs)

  def getBatchSize(self):
    return self._getBatchSize(self._Settings)