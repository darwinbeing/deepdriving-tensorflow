from ..internal import CBaseFactory
from .CReader import CReader

class CFactory(CBaseFactory):
  def __init__(self, ReaderClass):
    super().__init__(ReaderClass, CReader)

  def create(self, Settings = None, IsTraining = False, UsePreprocessing=True, UseDataAugmentation=True):
    return self._Class(Settings, IsTraining, UsePreprocessing, UseDataAugmentation)
