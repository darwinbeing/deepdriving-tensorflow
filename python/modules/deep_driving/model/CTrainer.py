import deep_learning as dl
import tensorflow as tf


class CTrainer(dl.trainer.CTrainer):

  def _createOptimizer(self, ErrorMeasurement, Settings):
    OptimizerSettings = Settings['Optimizer']
    TrainerSettings   = Settings['Trainer']
    DataSettings      = Settings['Data']

    with tf.name_scope("Optimizer"):
      CurrentOptimizationStep = tf.Variable(0, trainable=False, name="Step")

      IterationsPerEpoch = dl.helpers.getIterationsPerEpoch(TrainerSettings['EpochSize'], DataSettings['BatchSize'])

      LearnRate = tf.train.exponential_decay(
        learning_rate=OptimizerSettings['StartingLearningRate'],
        global_step=CurrentOptimizationStep,
        decay_steps=OptimizerSettings['EpochsPerDecay'] * IterationsPerEpoch,
        decay_rate=OptimizerSettings['LearnRateDecay'],
        staircase=True)

      tf.summary.scalar("LearnRate", LearnRate)
      tf.summary.scalar("Step", CurrentOptimizationStep)

      Optimizer = tf.train.AdamOptimizer(learning_rate=LearnRate)
      #Optimizer = tf.train.AdadeltaOptimizer(learning_rate=1.0)
      #Optimizer = tf.train.MomentumOptimizer(learning_rate=LearnRate, momentum=Settings['Optimizer']['Momentum'], use_nesterov = True)
      Gradients = Optimizer.compute_gradients(ErrorMeasurement.getOutputs()['Loss'])

      print("Apply individual learning rate scales...")
      ScaledGradients = []
      for Gradient, Variable in Gradients:
        Scale = dl.layer.LearningRates.get(Variable.name)
        if Scale != None:
          Gradient *= Scale
          print(" * \"{}\" has scale {}".format(Variable.name, Scale))

        ScaledGradients.append((Gradient, Variable))

      UpdateOperations = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
      with tf.control_dependencies(UpdateOperations):
        ApplyGradients = Optimizer.apply_gradients(ScaledGradients, global_step=CurrentOptimizationStep)

    return ApplyGradients

  def _trainIteration(self, Session, RunTargets, Reader, Iteration, Batch, Epoch):
    Data = Reader.readBatch(Session)
    AllTargets = RunTargets
    return Session.run(AllTargets, feed_dict = Data)

