from ..internal import CBaseFactory
from .CEvaluator import CEvaluator

class CFactory(CBaseFactory):
  def __init__(self, Class):
    super().__init__(Class, CEvaluator)

  def create(self, Network, Reader, ErrorMeas, Settings = None):
    return self._Class(Network, Reader, ErrorMeas, Settings)