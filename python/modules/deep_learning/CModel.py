from . import data
from . import error
from . import evaluator
from . import trainer
from . import internal
from . import network


class CModel():
  def __init__(self, Factory):
    self._NetworkFactory = internal.getFactory(Factory, network.CFactory, network.CNetwork)

  def createTrainer(self, TrainerFactoryArg, ReaderFactoryArg, ErrorMeasFactoryArg, Settings = None):
    TrainerFactory   = internal.getFactory(TrainerFactoryArg, trainer.CFactory, trainer.CTrainer)
    ReaderFactory    = internal.getFactory(ReaderFactoryArg, data.CFactory, data.CReader)
    ErrorMeasFactory = internal.getFactory(ErrorMeasFactoryArg, error.CFactory, error.CMeasurement)

    Reader  = ReaderFactory.create(Settings, IsTraining = True)
    Network = self._NetworkFactory.create(Reader, 0, Settings)
    ErrorMeas = ErrorMeasFactory.create(Network, Reader, Settings)

    Trainer = TrainerFactory.create(Network, Reader, ErrorMeas, Settings)

    return Trainer


  def createEvaluator(self, EvalautorFactoryArg, ReaderFactoryArg, ErrorMeasFactoryArg, Settings = None):
    EvaluatorFactory   = internal.getFactory(EvalautorFactoryArg, evaluator.CFactory, evaluator.CEvaluator)
    ReaderFactory      = internal.getFactory(ReaderFactoryArg, data.CFactory, data.CReader)
    ErrorMeasFactory   = internal.getFactory(ErrorMeasFactoryArg, error.CFactory, error.CMeasurement)

    Reader  = ReaderFactory.create(Settings, IsTraining = False)
    Network = self._NetworkFactory.create(Reader, 0, Settings)
    ErrorMeas = ErrorMeasFactory.create(Network, Reader, Settings)

    Evaluator = EvaluatorFactory.create(Network, Reader, ErrorMeas, Settings)

    return Evaluator

