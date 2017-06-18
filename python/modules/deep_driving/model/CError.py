import deep_learning as dl
import tensorflow as tf

from .. import db

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

  _Name = [
    "Angle",
    "L",
    "M",
    "R",
    "DistL",
    "DistR",
    "LL",
    "ML",
    "MR",
    "RR",
    "DistLL",
    "DistMM",
    "DistRR",
    "Fast",
  ]

  # Custom Methods
  def _buildLoss(self, Output, Label, Lambda):
    with tf.name_scope("Loss"):
      print("Create Loss Function...")

      NormLabel = db.normalizeLabels(Label)

      if dl.layer.Setup.StoreOutputAsText:
        ValueTable = dl.helpers.CTable(Header=["Type"]+self._Name)
        ValueTable.addLine(Line=["Output"]+Output)
        ValueTable.addLine(Line=["Label"]+NormLabel)

      Loss     = []
      MeanLoss = []
      SquaredLoss = None
      for i, Out in enumerate(Output):
        SingleSquaredLoss = tf.square(NormLabel[i] - Output[i])

        Loss.append(SingleSquaredLoss[0,:])
        MeanLoss.append(tf.reduce_mean(SingleSquaredLoss))

        if SquaredLoss is None:
          SquaredLoss = SingleSquaredLoss
        else:
          SquaredLoss = SquaredLoss + SingleSquaredLoss

      if dl.layer.Setup.StoreOutputAsText:
        ValueTable.addLine(Line=["Loss"]+Loss)
        ValueTable.addLine(Line=["MeanLoss"]+MeanLoss)
        tf.summary.text("Values", ValueTable.build())

      print("* Squared Loss shape: {}".format(SquaredLoss.shape))

      WeightDecayList = tf.get_collection('Losses')
      if len(WeightDecayList) > 0:
        WeightDecay = tf.add_n(WeightDecayList, name='WeightDecay')
      else:
        WeightDecay = 0

      Loss = tf.reduce_mean(SquaredLoss) + WeightDecay * Lambda

      tf.summary.scalar('LabelLoss', tf.reduce_mean(SquaredLoss))
      tf.summary.scalar('Loss', Loss)
      tf.summary.scalar('WeightDecayTerm', WeightDecay)
      tf.summary.scalar('WeightDecayRate', Lambda)
      return Loss


  def _buildError(self, NormOutput, Label):
    with tf.name_scope("DetailError"):
      print("Create Mean Absolute Error Function...")

      Output = db.denormalizeLabels(NormOutput)

      if dl.layer.Setup.StoreOutputAsText:
        ValueTable = dl.helpers.CTable(Header=["Type"]+self._Name)
        ValueTable.addLine(Line=["Output"]+Output)
        ValueTable.addLine(Line=["Label"]+Label)

      Errors = []
      Means  = []
      SDs    = []
      AbsoluteError = None
      for i, Out in enumerate(Output):
        SingleError = tf.abs(Label[i] - Output[i])
        Errors.append(SingleError)

        Mean, Var = tf.nn.moments(SingleError, axes=[0])
        Means.append(Mean)
        SDs.append(tf.sqrt(Var))
        tf.summary.scalar('{}_MAE'.format(self._Name[i]), tf.reshape(Mean, shape=[]))
        tf.summary.scalar('{}_SD'.format(self._Name[i]),  tf.sqrt(tf.reshape(Var, shape=[])))

        if AbsoluteError is None:
          AbsoluteError = SingleError
        else:
          AbsoluteError = AbsoluteError + SingleError

      if dl.layer.Setup.StoreOutputAsText:
        ValueTable.addLine(Line=["AE"]+Errors)
        ValueTable.addLine(Line=["MAE"]+Means)
        ValueTable.addLine(Line=["SD"]+SDs)
        tf.summary.text("Values", ValueTable.build())


    with tf.name_scope("Error"):
      print("* Absolute Error shape: {}".format(AbsoluteError.shape))

      Mean, Var = tf.nn.moments(AbsoluteError, axes=[0])

      tf.summary.scalar('MeanAbsoluteError', tf.reshape(Mean, shape=[]))
      tf.summary.scalar('StandardDeviation', tf.sqrt(tf.reshape(Var , shape=[])))

    return tf.reshape(Mean, shape=[])