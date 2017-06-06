from ..internal import CBaseFactory
from .CTrainer import CTrainer
from .. import helpers

class CFactory(CBaseFactory):
  def __init__(self, ReaderClass):
    super().__init__(ReaderClass, CTrainer)

  def create(self, Network, Reader, ErrorMeas, Settings = None):
    return self._Class(Network, Reader, ErrorMeas, Settings)