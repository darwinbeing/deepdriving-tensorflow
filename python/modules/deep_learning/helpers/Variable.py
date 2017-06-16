import tensorflow as tf

from tensorflow.contrib.layers import xavier_initializer_conv2d    as XavierInitializerConv
from tensorflow.contrib.layers import xavier_initializer           as XavierInitializer
from tensorflow                import truncated_normal_initializer as NormalInitializer
from tensorflow                import constant_initializer         as ConstantInitializer

def createVariable(Shape, Initializer = XavierInitializer(), WeightDecayFactor = 1.0, LearningRate=1.0, Name = "Weights", WeightDecayCollection="Losses"):
  """Helper to create an initialized Variable with weight decay.
  Note that the Variable is initialized with a truncated normal distribution.
  A weight decay is added only if one is specified.
  
  Args:
    Shape:             List of ints to define the shape of the variable.
    Initializer:       The initializer to use.
    WeightDecayFactor: Add L2-Loss weight decay multiplied by this float. If None, weight
                       decay is not added for this Variable.
    LearningRate:      A learning rate scaler.
    Name:              Name of the variable.
        
  Returns:
    Variable Tensor
    
  Note: This function was originally taken from: 
  https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10.py
  """

  Type     = tf.float32
  Variable = tf.Variable(initial_value=Initializer(shape=Shape), name=Name, dtype=Type)

  from ..layer import LearningRates
  if LearningRate != 1.0:
    LearningRates.set(Variable.name, LearningRate)

  if WeightDecayFactor is not None:
    WeightDecay = tf.multiply(tf.nn.l2_loss(Variable), WeightDecayFactor, name='WeightDecay')
    tf.add_to_collection(WeightDecayCollection, WeightDecay)

  tf.summary.scalar(Variable.name + '/sparsity', tf.nn.zero_fraction(Variable))

  return Variable


def createKernel2D(Shape, Initializer = XavierInitializerConv(), WeightDecayFactor = 1.0, LearningRate=1.0, Name = "Kernel", WeightDecayCollection = "Losses"):
  return createVariable(Shape, Initializer, WeightDecayFactor, LearningRate, Name, WeightDecayCollection)


def createBias(Shape, Initializer = ConstantInitializer(0), WeightDecayFactor = None, LearningRate=1.0, Name = "Biases", WeightDecayCollection = "Losses"):
  return createVariable(Shape, Initializer, WeightDecayFactor, LearningRate, Name, WeightDecayCollection)
