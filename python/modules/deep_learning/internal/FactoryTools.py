import inspect

import debug

def getFactory(Argument, DefaultFactory, Subclass):
  if inspect.isclass(Argument):
    Class = Argument
    debug.Assert(issubclass(Class, Subclass),
                 "You must specify a {}-Object or a {}-Class as network!".format(DefaultFactory.__name__, Subclass.__name__))
    return DefaultFactory(Class)

  else:
    Factory = Argument
    debug.Assert(isinstance(Factory, DefaultFactory),
                 "You must specify a {}-Object or a {}-Class as network!".format(DefaultFactory.__name__, Subclass.__name__))
    return Factory