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

import math

from .Table import getTableHeader, getTableLine, getTableMean, getTableSD, getTableMeanRef, getTableSDRef

class CErrorCalculator():

  _Errors = {
    'Angle': [],
    'Fast': [],
    'LL': [],
    'ML': [],
    'MR': [],
    'RR': [],
    'DistLL': [],
    'DistMM': [],
    'DistRR': [],
    'L': [],
    'M': [],
    'R': [],
    'DistL': [],
    'DistR': [],
  }
  _SD = {}
  _MAE = {}
  _IsReady = False
  def __init__(self):
    self.reset()


  def reset(self):
    self._Errors = {
      'Angle': [],
      'Fast': [],
      'LL': [],
      'ML': [],
      'MR': [],
      'RR': [],
      'DistLL': [],
      'DistMM': [],
      'DistRR': [],
      'L': [],
      'M': [],
      'R': [],
      'DistL': [],
      'DistR': [],
    }
    self._SD = {}
    self._MAE = {}
    self._IsReady = False


  def add(self, Real, Estimated):
    self._IsReady = False
    self._addError("Angle", Real, Estimated)
    self._addError("Fast", Real, Estimated)
    self._addError("LL", Real, Estimated)
    self._addError("ML", Real, Estimated)
    self._addError("MR", Real, Estimated)
    self._addError("RR", Real, Estimated)
    self._addError("DistLL", Real, Estimated)
    self._addError("DistMM", Real, Estimated)
    self._addError("DistRR", Real, Estimated)
    self._addError("L", Real, Estimated)
    self._addError("M", Real, Estimated)
    self._addError("R", Real, Estimated)
    self._addError("DistL", Real, Estimated)
    self._addError("DistR", Real, Estimated)


  def _addError(self, Type, Real, Estimated):
    self._Errors[Type].append(abs(Real[Type] - Estimated[Type]))


  def getMAE(self):
    if self._IsReady:
      return self._MAE
    else:
      self.calc()
      return self._MAE


  def getSD(self):
    if self._IsReady:
      return self._SD
    else:
      self.calc()
      return self._SD


  def getN(self):
    return len(self._Errors["Angle"])


  def calc(self):
    self._calcMAE()
    self._calcAllSD()
    self._IsReady = True


  def _calcMAE(self):
    self._calcMean("Angle")
    self._calcMean("Fast")
    self._calcMean("LL")
    self._calcMean("ML")
    self._calcMean("MR")
    self._calcMean("RR")
    self._calcMean("DistLL")
    self._calcMean("DistMM")
    self._calcMean("DistRR")
    self._calcMean("L")
    self._calcMean("M")
    self._calcMean("R")
    self._calcMean("DistL")
    self._calcMean("DistR")


  def _calcMean(self, Type):
    N = len(self._Errors[Type])
    Sum = 0.0
    for Error in self._Errors[Type]:
      Sum += Error

    self._MAE[Type] = Sum/N


  def _calcAllSD(self):
    self._calcSD("Angle")
    self._calcSD("Fast")
    self._calcSD("LL")
    self._calcSD("ML")
    self._calcSD("MR")
    self._calcSD("RR")
    self._calcSD("DistLL")
    self._calcSD("DistMM")
    self._calcSD("DistRR")
    self._calcSD("L")
    self._calcSD("M")
    self._calcSD("R")
    self._calcSD("DistL")
    self._calcSD("DistR")


  def _calcSD(self, Type):
    N = len(self._Errors[Type])
    VarSum = 0.0
    for Error in self._Errors[Type]:
      VarSum += (Error - self._MAE[Type]) * (Error - self._MAE[Type])

    self._SD[Type] = math.sqrt(VarSum/N)


  def __str__(self):
    if self.getN() > 0:
      ProgressString = ""
      ProgressString += getTableHeader(8)+"\n"
      ProgressString += getTableLine(8)+"\n"
      ProgressString += getTableMean(self.getMAE(), 8)+"\n"
      ProgressString += getTableSD(self.getSD(), 8)+"\n"
      ProgressString += getTableLine(8)+"\n"
      ProgressString += getTableMeanRef(self.getMAE(), 8)+"\n"
      ProgressString += getTableSDRef(self.getSD(), 8)+"\n"
      return ProgressString

    return ""
