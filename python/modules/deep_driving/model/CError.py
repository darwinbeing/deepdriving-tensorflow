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

      OneHotLabels    = Label

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


  def _buildError(self, Output, Label):
    with tf.name_scope("ClassError"):
      print("Create Error-Measurement Function...")

      print(" * Output-Class Shape: {}".format(Output.shape))

      IsWrong = 1.0 - tf.reduce_mean(tf.cast(tf.equal(Output, Label), tf.float32), axis=1)

      print(" * Sample Classification Error Shape: {}".format(IsWrong.shape))

      ClassificationError = tf.reduce_mean(IsWrong, axis=0)

      tf.summary.scalar('Error', ClassificationError)
      return ClassificationError