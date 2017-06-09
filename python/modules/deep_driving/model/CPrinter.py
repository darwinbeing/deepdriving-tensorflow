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

class CPrinter(deep_learning.printer.CProgressPrinter):
  def __init__(self):
    super().__init__(LossName="Loss/Loss")


  def _getErrorString(self, SummaryDict):
    ProgressString = ""
    Error = self._getValueFromKey(SummaryDict, "Error/MeanAbsoluteError")

    if Error != None:
      ProgressString += " Error: {:.2f}".format(Error)

    return ProgressString


  def _printFullSummaryDict(self, SummaryDict):
    ProgressString = "Full Summary:  ("
    ProgressString += self._getErrorString(SummaryDict)+", "
    ProgressString += " SD: {:.2f}".format(SummaryDict['Error/StandardDeviation'])
    ProgressString += " )\n\n"
    ProgressString += self._getTableHeader(8)+"\n"
    ProgressString += self._getTableLine(8)+"\n"
    ProgressString += self._getTableMean(SummaryDict, 8)+"\n"
    ProgressString += self._getTableSD(SummaryDict, 8)+"\n"
    ProgressString += self._getTableLine(8)+"\n"
    ProgressString += self._getTableMeanRef(SummaryDict, 8)+"\n"
    ProgressString += self._getTableSDRef(SummaryDict, 8)+"\n"
    print(ProgressString)


  def _getTableHeader(self, CellWidth):
    ProgressString = "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("Type") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("Angle") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("LL") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("ML") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("MR") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("RR") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("DistLL") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("DistMM") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("DistRR") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("L") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("M") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("R") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("DistL") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("DistR") + "|"
    ProgressString += str("{:^"+str(CellWidth)+"}").format("Fast") + "|"
    return ProgressString


  def _getTableLine(self, CellWidth):
    ProgressString = "+"
    for i in range(15):
      ProgressString += str("{:-^"+str(CellWidth)+"}").format("") + "+"
    return ProgressString


  def _getTableMean(self, Dict, CellWidth):
    CellWidth -= 1
    ProgressString = "|"
    ProgressString += str("{:^"+str(CellWidth+1)+"}").format("MAE") + "|"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/Angle_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/LL_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/ML_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/MR_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/RR_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistLL_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistMM_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistRR_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/L_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/M_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/R_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistL_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistR_MAE']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/Fast_MAE']) + " |"
    return ProgressString


  def _getTableMeanRef(self, Dict, CellWidth):
    # Reference values taken from:
    # "Extracting Cognition out of Images for the Purpose of Autonomous Driving".
    # PhD Thesis of Chenyi Chen. May 2016.
    CellWidth -= 2
    ProgressString = "|"
    ProgressString += str("{:^"+str(CellWidth+2)+"}").format("MAE/Ref") + "|"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/Angle_MAE']/0.033) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/LL_MAE']/0.188) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/ML_MAE']/0.155) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/MR_MAE']/0.159) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/RR_MAE']/0.183) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistLL_MAE']/5.085) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistMM_MAE']/4.738) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistRR_MAE']/7.983) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/L_MAE']/0.316) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/M_MAE']/0.308) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/R_MAE']/0.294) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistL_MAE']/8.910) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistR_MAE']/10.861) + "% |"
    #ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/Fast_MAE']) + "% |"
    ProgressString += str("{:>" + str(CellWidth) + "}").format("N/A ") + "% |"
    return ProgressString


  def _getTableSD(self, Dict, CellWidth):
    CellWidth -= 1
    ProgressString = "|"
    ProgressString += str("{:^"+str(CellWidth+1)+"}").format("SD") + "|"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/Angle_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/LL_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/ML_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/MR_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/RR_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistLL_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistMM_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistRR_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/L_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/M_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/R_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistL_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/DistR_SD']) + " |"
    ProgressString += str("{:>"+str(CellWidth)+".2f}").format(Dict['DetailError/Fast_SD']) + " |"
    return ProgressString

  def _getTableSDRef(self, Dict, CellWidth):
    # Reference values taken from:
    # "Extracting Cognition out of Images for the Purpose of Autonomous Driving".
    # PhD Thesis of Chenyi Chen. May 2016.
    CellWidth -= 2
    ProgressString = "|"
    ProgressString += str("{:^"+str(CellWidth+2)+"}").format("SD/Ref") + "|"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/Angle_SD']/0.086) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/LL_SD']/0.544) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/ML_SD']/0.415) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/MR_SD']/0.444) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/RR_SD']/0.528) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistLL_SD']/9.105) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistMM_SD']/7.816) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistRR_SD']/12.577) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/L_SD']/0.704) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/M_SD']/0.719) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/R_SD']/0.548) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistL_SD']/12.925) + "% |"
    ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/DistR_SD']/14.640) + "% |"
    #ProgressString += str("{:>"+str(CellWidth)+".1f}").format(100*Dict['DetailError/Fast_SD']) + "% |"
    ProgressString += str("{:>" + str(CellWidth) + "}").format("N/A ") + "% |"
    return ProgressString
