import debug

from .. import data
from .. import helpers


class CNetwork():
  def __init__(self, Reader, Settings = None):
    if Settings is None:
      self._Settings = {}
    else:
      self._Settings = Settings
    self._Reader = Reader

    debug.Assert(isinstance(self._Reader, data.CReader), "The Reader argument must be an object ")

    self._IsReady = False
    self._Structure = {}

    self._buildGraph()


  def _buildGraph(self):
    if self._IsReady == False:
      Inputs = self._Reader.getOutputs()
      self._Structure = self._build(Inputs, self._Settings)

      self._IsReady = True


  def getOutputs(self):
    return self._getOutputs(self._Structure)


  def _build(self, Inputs, Settings):
    import inspect
    raise Exception("You must overwrite the method {} of {}!".format(inspect.stack()[0][3], __name__))
    # Overwrite this method to build your network and return the structure
    return {}


  def _getOutputs(self, Structure):
    import inspect
    raise Exception("You must overwrite the method {} of {}!".format(inspect.stack()[0][3], __name__))
    # Returns a dict of output signals, used for inference
    return {}
