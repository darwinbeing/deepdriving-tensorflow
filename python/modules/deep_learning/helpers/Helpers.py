import math
import tensorflow as tf
import numpy as np

import debug

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


def checkVersion(Major, Minor):
  Version = tf.__version__.split('.')
  IsVersonOk = False

  if int(Version[0]) > Major:
    IsVersonOk=True
  elif int(Version[0]) == Major:
    IsVersonOk=(int(Version[1]) >= Minor)

  if not IsVersonOk:
    debug.logWarning("Tensorflow Version is {}.{}, but any feature expects at least {}.{}. This feature will be disabled.".format(Version[0], Version[1], Major, Minor))

  return IsVersonOk