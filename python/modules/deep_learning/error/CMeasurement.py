import debug

from .. import data
from .. import network


class CMeasurement():
  def __init__(self, Network, Reader, Settings = None):
    debug.Assert(isinstance(Network, network.CNetwork), "You must specify a Network object.")
    debug.Assert(isinstance(Reader, data.CReader), "You must specify a Reader object.")
    self._Network = Network
    self._Reader = Reader
    if Settings == None:
      self._Settings = {}
    else:
      self._Settings = Settings

    self._IsReady = False
    self._Strcture = {}

    self._prepare()


  def _prepare(self):
    if not self._IsReady:
      self._Strcture = self._build(self._Network, self._Reader, self._Settings)
      self._IsReady = True


  def getOutputs(self):
    return self._getOutputs(self._Strcture)


  def getEvalError(self):
    return self._getEvalError(self._Strcture)


  def _getOutputs(self, Structure):
    raise Exception("You must overwrite this method to return error-measurement outputs!")
    return {}


  def _getEvalError(self, Structure):
    raise Exception("You must overwrite this method to return the evaluation error operation!")
    return None


  def _build(self, Network, Reader, Settings):
    raise Exception("You must overwrite this method to build the error-measurement and output the structure!")
    return {}