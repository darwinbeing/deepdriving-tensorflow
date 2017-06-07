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
      print("Create Loss Function...")

      SquaredLoss = None
      for i, Out in enumerate(Output):
        SingleSquaredLoss = tf.square(Label[i] - Output[i])
        if SquaredLoss is None:
          SquaredLoss = SingleSquaredLoss
        else:
          SquaredLoss = SquaredLoss + SingleSquaredLoss

      print("* Squared Loss shape: {}".format(SquaredLoss.shape))

      WeightDecayList = tf.get_collection('Losses')
      if len(WeightDecayList) > 0:
        WeightDecay = tf.add_n(WeightDecayList, name='WeightDecay')
      else:
        WeightDecay = 0

      Loss = tf.reduce_mean(SquaredLoss) + WeightDecay * Lambda

      tf.summary.scalar('Loss', Loss)
      tf.summary.scalar('WeightDecayTerm', WeightDecay)
      tf.summary.scalar('WeightDecayRate', Lambda)
      return Loss


  def _buildError(self, Output, Label):
    with tf.name_scope("Error"):
      print("Create Mean Absolute Error Function...")

      AbsoluteError = None
      for i, Out in enumerate(Output):
        SingleError = tf.abs(Label[i] - Output[i])
        if AbsoluteError is None:
          AbsoluteError = SingleError
        else:
          AbsoluteError = AbsoluteError + SingleError

      print("* Absolute Error shape: {}".format(AbsoluteError.shape))

      MeanAbsolutError = tf.reduce_mean(AbsoluteError)

      Mean, Var = tf.nn.moments(AbsoluteError, axes=[0])

      Mean = tf.reshape(Mean, shape=[])
      Var  = tf.reshape(Var , shape=[])

      tf.summary.scalar('MAE', MeanAbsolutError)
      tf.summary.scalar('MeanAbsolutError', Mean)
      tf.summary.scalar('StandardDeviaton', tf.sqrt(Var))

      return MeanAbsolutError