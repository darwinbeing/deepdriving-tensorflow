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

import deep_learning
from .. import error

NameDictMAE = {
  'Angle': 'DetailError/Angle_MAE',
  'Fast': 'DetailError/Fast_MAE',
  'LL': 'DetailError/LL_MAE',
  'ML': 'DetailError/ML_MAE',
  'MR': 'DetailError/MR_MAE',
  'RR': 'DetailError/RR_MAE',
  'DistLL': 'DetailError/DistLL_MAE',
  'DistMM': 'DetailError/DistMM_MAE',
  'DistRR': 'DetailError/DistRR_MAE',
  'L': 'DetailError/L_MAE',
  'M': 'DetailError/M_MAE',
  'R': 'DetailError/R_MAE',
  'DistL': 'DetailError/DistL_MAE',
  'DistR': 'DetailError/DistR_MAE'
}

NameDictSD = {
  'Angle': 'DetailError/Angle_SD',
  'Fast': 'DetailError/Fast_SD',
  'LL': 'DetailError/LL_SD',
  'ML': 'DetailError/ML_SD',
  'MR': 'DetailError/MR_SD',
  'RR': 'DetailError/RR_SD',
  'DistLL': 'DetailError/DistLL_SD',
  'DistMM': 'DetailError/DistMM_SD',
  'DistRR': 'DetailError/DistRR_SD',
  'L': 'DetailError/L_SD',
  'M': 'DetailError/M_SD',
  'R': 'DetailError/R_SD',
  'DistL': 'DetailError/DistL_SD',
  'DistR': 'DetailError/DistR_SD'
}

class CPrinter(deep_learning.printer.CProgressPrinter):
  def __init__(self):
    super().__init__(LossName="Loss/LabelLoss")


  def _getErrorString(self, SummaryDict):
    ProgressString = ""
    Error = self._getValueFromKey(SummaryDict, "Error/MeanAbsoluteError")

    if Error != None:
      ProgressString += " Error: {:.2f}".format(Error)

    return ProgressString


  def _getFullSummaryDict(self, SummaryDict):
    ProgressString = "Full Summary:  ("
    ProgressString += self._getErrorString(SummaryDict)+", "
    ProgressString += " SD: {:.2f}".format(SummaryDict['Error/StandardDeviation'])
    ProgressString += " )\n\n"
    ProgressString += error.getTableHeader(8)+"\n"
    ProgressString += error.getTableLine(8)+"\n"
    ProgressString += error.getTableMean(SummaryDict, 8, NameDictMAE)+"\n"
    ProgressString += error.getTableSD(SummaryDict, 8, NameDictSD)+"\n"
    ProgressString += error.getTableLine(8)+"\n"
    ProgressString += error.getTableMeanRef(SummaryDict, 8, NameDictMAE)+"\n"
    ProgressString += error.getTableSDRef(SummaryDict, 8, NameDictSD)+"\n"
    return ProgressString
