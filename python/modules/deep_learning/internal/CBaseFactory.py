import inspect

import debug

class CBaseFactory():
  def __init__(self, Class, TargetClass):
    debug.Assert(inspect.isclass(Class), "You must specify a class as argument.")
    debug.Assert(issubclass(Class, TargetClass), "The class is not a subclass of {}".format(TargetClass.__name__))
    self._Class = Class

  def create(self):
    return self._Class()