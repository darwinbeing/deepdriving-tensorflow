# The MIT license:
#
# Copyright 2017 Andre Netzeband
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#
# Note: The DeepDriving project on this repository is derived from the DeepDriving project devloped by the princeton 
# university (http://deepdriving.cs.princeton.edu/). The above license only applies to the parts of the code, which 
# were not a derivative of the original DeepDriving project. For the derived parts, the original license and 
# copyright is still valid. Keep this in mind, when using code from this project.

import tensorflow as tf

from .. import helpers

from .Setup import Setup

def createActivation(Input, Func="ReLU", Name=None):

  UseFunc = tf.identity
  if Func == "ID" or Func == "id":
    UseFunc = tf.identity

  elif Func == "ReLU" or Func == "relu":
    UseFunc = tf.nn.relu

  elif Func == "PReLU" or Func == "prelu":
    UseFunc = lambda Input, name: tf.contrib.keras.layers.PReLU()(Input)

  elif Func == "Tanh" or Func == "tanh":
    UseFunc = tf.tanh

  elif Func == "Sigmoid" or Func == "sigmoid":
    UseFunc = tf.sigmoid

  else:
    debug.LogError("Unknown activation function: {}".formati(Func))

  if Name != None:
    Setup.Log(" * Create Activation-Layer {} with Function {}".format(Name, Func))

  A = UseFunc(Input, name=Name)
  if Setup.StoreHistogram:
    tf.summary.histogram("Activation", A)

  if Setup.StoreSparsity:
    tf.summary.scalar("Activation/Sparsity", tf.nn.zero_fraction(A))

  return A