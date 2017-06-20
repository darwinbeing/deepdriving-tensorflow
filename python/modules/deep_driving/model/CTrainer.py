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

      #Optimizer = tf.train.AdamOptimizer(learning_rate=LearnRate)
      Optimizer = tf.train.AdadeltaOptimizer(learning_rate=LearnRate)
      #Optimizer = tf.train.MomentumOptimizer(learning_rate=LearnRate, momentum=Settings['Optimizer']['Momentum'], use_nesterov = True)
      Gradients = Optimizer.compute_gradients(ErrorMeasurement.getOutputs()['Loss'])


      GradientNoise = self._getGradientNoise(Settings)
      if GradientNoise is not None:
        NoisyGradients = []
        print("Apply noise to gradients (nu = {})...".format(GradientNoise))
        # Taken from: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/layers/python/layers/optimizers.py
        for Gradient, Variable in Gradients:
          if Gradient is not None:
            if isinstance(Gradient, tf.IndexedSlices):
              GradientShape = Gradient.dense_shape
            else:
              GradientShape = Gradient.get_shape()

            Noise = tf.truncated_normal(GradientShape) * ( GradientNoise / ( tf.sqrt(tf.cast((CurrentOptimizationStep + 1), tf.float32)) ) )
            Gradient += Noise

          NoisyGradients.append((Gradient, Variable))

      else:
        NoisyGradients = Gradients


      print("Apply individual learning rate scales...")
      ScaledGradients = []
      for Gradient, Variable in NoisyGradients:
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


  def _getGradientNoise(self, Settings):
    if "Trainer" in Settings:
      if "Noise" in Settings["Trainer"]:
        return Settings["Trainer"]["Noise"]

    return None