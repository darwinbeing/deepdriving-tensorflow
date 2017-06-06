import math
import tensorflow as tf
import numpy as np

def getShapeList(TensorflowShape):
  ShapeList = []
  for Shape in TensorflowShape:
    ShapeList.append(int(Shape))

  return ShapeList

def getIterationsPerEpoch(EpochSize, BatchSize):
  return int(math.ceil(EpochSize / BatchSize))

def getTrainableVariables():
  Variables = 0
  Tensors   = 0
  for Tensor in tf.global_variables():
    Tensors += 1
    Variables += np.prod(Tensor.get_shape().as_list())

  return Variables, Tensors

def getTrainableVariablesInScope(ScopeName):
  Variables = 0
  Tensors   = 0
  for Tensor in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=ScopeName):
    Tensors += 1
    Variables += np.prod(Tensor.get_shape().as_list())

  return Variables, Tensors
