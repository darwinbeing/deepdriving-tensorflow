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

import deep_learning as dl
import dd

from .. import db

class CInference(dl.inference.CInference):

  def _runIteration(self, Session, RunTargets, Inputs, Reader, Iteration):
    Data = Reader.readSingle(Session, Inputs)
    AllTargets = self._Network.getOutputs()['Output']
    return Session.run(AllTargets, feed_dict = Data)

  def _postProcess(self, Results):
    RealResults = db.denormalizeLabels(Results)

    Indicators = dd.Indicators_t()
    Indicators.Speed  = 0.0
    Indicators.Fast   = RealResults[13]
    Indicators.Angle  = RealResults[0]
    Indicators.LL     = RealResults[6]
    Indicators.ML     = RealResults[7]
    Indicators.MR     = RealResults[8]
    Indicators.RR     = RealResults[9]
    Indicators.DistLL = RealResults[10]
    Indicators.DistMM = RealResults[11]
    Indicators.DistRR = RealResults[12]
    Indicators.L      = RealResults[1]
    Indicators.M      = RealResults[2]
    Indicators.R      = RealResults[3]
    Indicators.DistL  = RealResults[4]
    Indicators.DistR  = RealResults[5]

    return Indicators