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

import debug
import tensorflow as tf
import misc.arguments as args

from .CLayer import CLayer
from ..Setup import Setup

class CNewLayerName():
  def __init__(self, Sequence, Name, UseCounter):
    self._Sequence   = Sequence
    self._Name       = Name
    self._UseCounter = UseCounter

  def __enter__(self):
    return self._Name

  def __exit__(self, type, value, traceback):
    self._Sequence.addLayerName(None, False)

  @property
  def Name(self):
    return self._Name

  @property
  def UseCounter(self):
    return self._UseCounter


class CSequence(CLayer):
  """
  This class represents a sequence of layers.
  """

  def __init__(self, Name = None, Layers = None, DefaultLayer = None):
    self._Name   = Name
    self._Layers = []
    self._DefaultLayer = DefaultLayer
    if Layers is not None:
      self.addLayers(Layers)


  def addLayers(self, Layers):
    if isinstance(Layers, list):
      for Layer in Layers:
        self.add(Layer)
    elif isinstance(Layers, CLayer):
      self.add(Layers)


  def add(self, Layer):
    AddedLayer = Layer.copy()
    self._Layers.append(AddedLayer)
    return AddedLayer


  def copy(self):
    New = CSequence()

    # copy attributes
    New._Name         = self._Name
    New._DefaultLayer = self._DefaultLayer

    # copy sub-layers
    New._Layers = []
    for Layer in self._Layers:
      New._Layers.append(Layer.copy())

    return New


  def __call__(self, *args, **kwargs):
    if self._DefaultLayer is None:
      return self._doCall(*args, **kwargs)

    else:
      New = self.copy()

      # extract name from kwargs
      try:
        New._Name = kwargs["Name"]
        del(kwargs["Name"])
      except:
        pass

      LayerIndex = New._getLayerIndex(New._DefaultLayer)
      DefaultLayer = New._Layers[LayerIndex]
      New._Layers[LayerIndex] = None
      New._Layers[LayerIndex] = DefaultLayer(*args, **kwargs)

      return New


  def _doCall(self, Name = args.NotSet, Layers = args.NotSet, DefaultLayer = args.NotSet):
    New = self.copy()

    if not args.isNotSet(Name):
      New._Name = Name

    if not args.isNotSet(Layers):
      New._Layers = []
      if Layers is not None:
        New.addLayers(Layers)

    if not args.isNotSet(DefaultLayer):
      New._DefaultLayer = DefaultLayer

    return New


  def addLayerName(self, Name, UseCounter=True):
    NameObject = CNewLayerName(self, Name, UseCounter)
    self._Layers.append(NameObject)
    return NameObject


  def __getitem__(self, Index):
    LayerIndex = self._getLayerIndex(Index)
    debug.Assert(LayerIndex != None, "Cannot find layer {} in sequence!".format(Index))
    return self._Layers[LayerIndex]


  def _getLayerIndex(self, Index):
    CurrentLayer = 0
    for i, Layer in enumerate(self._Layers):
      if not isinstance(Layer, CNewLayerName):
        if CurrentLayer == Index:
          return i

        else:
          CurrentLayer += 1

    return None


  def __getattr__(self, AttributeName):
    debug.Assert(self._DefaultLayer != None, "There is no default layer specified, thus I cannot pass function call \"{}(...)\" to it.".format(AttributeName))

    DefaultLayer = self[self._DefaultLayer]
    Method       = getattr(DefaultLayer, AttributeName)

    def CallWrapper(*args, **kw):
      Method(*args, **kw)
      return self

    return CallWrapper


  def apply(self, Signal):

    if self._Name is not None:
      Setup.log("* Apply sequence of {} layers with name \"{}\":".format(len(self._Layers), self._Name))
      Setup.increaseLoggerIndent(2)

      with tf.variable_scope(self._Name) as Scope:
        Signal = self._applyAll(Signal)

      Setup.decreaseLoggerIndent(2)

    else:
      Setup.log("* Apply sequence of {} layers:".format(len(self._Layers)))
      Signal = self._applyAll(Signal)

    return Signal


  def _applyAll(self, Signal):

    N       = len(self._Layers)
    i       = 0
    Counter = 0

    while i < N:
      Layer = self._Layers[i]

      if isinstance(Layer, CNewLayerName):
        if Layer.Name is not None:

          FullName = Layer.Name
          if (Layer.UseCounter):
            Counter += 1
            FullName = FullName + "_{}".format(Counter)

          Setup.log("*** Layer: {} ***".format(FullName))
          Setup.increaseLoggerIndent(2)
          with tf.variable_scope(FullName) as Scope:
            i += 1
            LeaveScope = False
            while (i < N) and (not LeaveScope):
              Layer = self._Layers[i]
              if not isinstance(Layer, CNewLayerName):
                Signal = Layer.apply(Signal)
                i += 1
              else:
                LeaveScope = True

          Setup.decreaseLoggerIndent(2)

        else:
          # None names can be ignored
          i += 1

      else:
        Signal = Layer.apply(Signal)
        i += 1

    return Signal
