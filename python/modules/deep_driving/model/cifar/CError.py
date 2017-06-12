import deep_learning as dl
import tensorflow as tf

class CError(dl.error.CMeasurement):
  def _build(self, Network, Reader, Settings):
    Structure = {}

    self._Lambda = Reader.getOutputs()['Lambda']
    Structure['Loss']  = self._buildLoss(Network.getOutputs()['Output'],  Reader.getOutputs()['Labels'], self._Lambda)
    Structure['Error'] = self._buildError(Network.getOutputs()['Output'], Reader.getOutputs()['Labels'])

    return Structure

  def _getOutputs(self, Structure):
    return Structure

  def _getEvalError(self, Structure):
    return Structure['Error']


  # Custom Methods
  def _buildLoss(self, Output, Label, Lambda):
    with tf.name_scope("Loss"):
      print("Create Cross-Entropy Loss Function...")
      print("* Label Shape: {}".format(Label.shape))

      NumberOfClasses = int(Output.shape[1])
      OneHotLabels = tf.one_hot(Label, depth=NumberOfClasses)

      print("* OneHot Label Shape: {}".format(OneHotLabels.shape))
      print("* Output Shape: {}".format(Output.shape))

      SampleCrossEntropy = tf.nn.softmax_cross_entropy_with_logits(labels=OneHotLabels, logits=Output, name="SoftmaxLoss")

      WeightDecayList = tf.get_collection('Losses')
      if len(WeightDecayList) > 0:
        WeightDecay = tf.add_n(WeightDecayList, name='WeightDecay')
      else:
        WeightDecay = 0

      print("* Sample Loss Shape: {}".format(SampleCrossEntropy.shape))
      Loss = tf.reduce_mean(SampleCrossEntropy) + WeightDecay * Lambda

      tf.summary.scalar('Loss', Loss)
      tf.summary.scalar('WeightDecayTerm', WeightDecay)
      tf.summary.scalar('WeightDecayRate', Lambda)

    return Loss

  _CatName = [
    "Plane",
    "Car",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck",
  ]

  def _buildError(self, Output, Label):
    with tf.name_scope("ClassError"):
      print("Create Error-Measurement Function...")

      OutputClass = tf.cast(tf.argmax(Output, axis=1), tf.int32)

      print(" * Output-Class Shape: {}".format(OutputClass.shape))

      IsWrong = 1.0 - tf.cast(tf.equal(OutputClass, Label), tf.float32)

      print(" * Sample Classification Error Shape: {}".format(IsWrong.shape))

      ClassificationError = tf.reduce_mean(IsWrong, axis=0)

      NumberOfClasses = int(Output.shape[1])
      OneHotLabels = tf.one_hot(Label, depth=NumberOfClasses)

      SoftmaxOutput = tf.nn.softmax(Output)

      if dl.layer.Setup.StoreOutputAsText:
        ValueTable = dl.helpers.CTable(["Type"]+self._CatName)
        ValueTable.addLine(Line=["Output"]+tf.split(SoftmaxOutput, 10, axis=1))
        ValueTable.addLine(Line=["Label"]+tf.split(OneHotLabels, 10, axis=1))
        tf.summary.text("Values", ValueTable.build())

      tf.summary.scalar('Error', ClassificationError)

    return ClassificationError

