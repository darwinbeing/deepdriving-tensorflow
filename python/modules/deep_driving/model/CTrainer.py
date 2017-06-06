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
      Gradients = Optimizer.compute_gradients(ErrorMeasurement.getOutputs()['Loss'])

      UpdateOperations = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
      with tf.control_dependencies(UpdateOperations):
        ApplyGradients = Optimizer.apply_gradients(Gradients, global_step=CurrentOptimizationStep)

    return ApplyGradients

  def _trainIteration(self, Session, RunTargets, Reader, Iteration, Batch, Epoch):
    Data = Reader.readBatch(Session)
    AllTargets = RunTargets
    return Session.run(AllTargets, feed_dict = Data)
