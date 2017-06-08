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

import debug
import deep_learning

class CMerger(deep_learning.summary.CMerger):
  def _mergeSummaries(self, Summaries, SummaryTool):
    #print("*** Merge {} Summaries...".format(len(Summaries)))

    N = len(Summaries)
    SummaryData = {
      "Loss/Loss": [],
      "Error/MeanAbsoluteError": [],
      "Error/StandardDeviation": [],
      "DetailError/Angle_MAE": [],
      "DetailError/Angle_SD": [],
      "DetailError/Fast_MAE": [],
      "DetailError/Fast_SD": [],
      "DetailError/LL_MAE": [],
      "DetailError/LL_SD": [],
      "DetailError/ML_MAE": [],
      "DetailError/ML_SD": [],
      "DetailError/MR_MAE": [],
      "DetailError/MR_SD": [],
      "DetailError/RR_MAE": [],
      "DetailError/RR_SD": [],
      "DetailError/DistLL_MAE": [],
      "DetailError/DistLL_SD": [],
      "DetailError/DistMM_MAE": [],
      "DetailError/DistMM_SD": [],
      "DetailError/DistRR_MAE": [],
      "DetailError/DistRR_SD": [],
      "DetailError/L_MAE": [],
      "DetailError/L_SD": [],
      "DetailError/M_MAE": [],
      "DetailError/M_SD": [],
      "DetailError/R_MAE": [],
      "DetailError/R_SD": [],
      "DetailError/DistL_MAE": [],
      "DetailError/DistL_SD": [],
      "DetailError/DistR_MAE": [],
      "DetailError/DistR_SD": [],
    }

    # collect all data
    for i, Summary in enumerate(Summaries):
      SummaryTool.ParseFromString(Summary)

      for Value in SummaryTool.value:
        for Key in SummaryData.keys():
          if Key in Value.tag:
            SummaryData[Key].append(Value.simple_value)

    for Key in SummaryData.keys():
      # ensure all data was collected
      debug.Assert(len(SummaryData[Key]) == N, "Was not able to collect enough data for key \"{}\" (only {} entries).".format(Key, len(SummaryData[Key])))

    SummaryData = self._mergeData(SummaryData, N)

    # write back values
    for Value in SummaryTool.value:
      for Key in SummaryData.keys():
        if Key in Value.tag:
          Value.simple_value = SummaryData[Key]

    Result = SummaryTool.SerializePartialToString()

    return Result

  def _mergeData(self, Data, N):
    Data["Loss/Loss"]               = self._mergeMean(Data["Loss/Loss"], N)
    Data["Error/StandardDeviation"] = self._mergeSD(Data["Error/StandardDeviation"], Data["Error/MeanAbsoluteError"], N)
    Data["Error/MeanAbsoluteError"] = self._mergeMean(Data["Error/MeanAbsoluteError"], N)
    Data["DetailError/Angle_SD"]    = self._mergeSD(Data["DetailError/Angle_SD"], Data["DetailError/Angle_MAE"], N)
    Data["DetailError/Angle_MAE"]   = self._mergeMean(Data["DetailError/Angle_MAE"], N)
    Data["DetailError/Fast_SD"]     = self._mergeSD(Data["DetailError/Fast_SD"], Data["DetailError/Fast_MAE"], N)
    Data["DetailError/Fast_MAE"]    = self._mergeMean(Data["DetailError/Fast_MAE"], N)
    Data["DetailError/LL_SD"]       = self._mergeSD(Data["DetailError/LL_SD"], Data["DetailError/LL_MAE"], N)
    Data["DetailError/LL_MAE"]      = self._mergeMean(Data["DetailError/LL_MAE"], N)
    Data["DetailError/ML_SD"]       = self._mergeSD(Data["DetailError/ML_SD"], Data["DetailError/ML_MAE"], N)
    Data["DetailError/ML_MAE"]      = self._mergeMean(Data["DetailError/ML_MAE"], N)
    Data["DetailError/MR_SD"]       = self._mergeSD(Data["DetailError/MR_SD"], Data["DetailError/MR_MAE"], N)
    Data["DetailError/MR_MAE"]      = self._mergeMean(Data["DetailError/MR_MAE"], N)
    Data["DetailError/RR_SD"]       = self._mergeSD(Data["DetailError/RR_SD"], Data["DetailError/RR_MAE"], N)
    Data["DetailError/RR_MAE"]      = self._mergeMean(Data["DetailError/RR_MAE"], N)
    Data["DetailError/DistLL_SD"]   = self._mergeSD(Data["DetailError/DistLL_SD"], Data["DetailError/DistLL_MAE"], N)
    Data["DetailError/DistLL_MAE"]  = self._mergeMean(Data["DetailError/DistLL_MAE"], N)
    Data["DetailError/DistMM_SD"]   = self._mergeSD(Data["DetailError/DistMM_SD"], Data["DetailError/DistMM_MAE"], N)
    Data["DetailError/DistMM_MAE"]  = self._mergeMean(Data["DetailError/DistMM_MAE"], N)
    Data["DetailError/DistRR_SD"]   = self._mergeSD(Data["DetailError/DistRR_SD"], Data["DetailError/DistRR_MAE"], N)
    Data["DetailError/DistRR_MAE"]  = self._mergeMean(Data["DetailError/DistRR_MAE"], N)
    Data["DetailError/L_SD"]        = self._mergeSD(Data["DetailError/L_SD"], Data["DetailError/L_MAE"], N)
    Data["DetailError/L_MAE"]       = self._mergeMean(Data["DetailError/L_MAE"], N)
    Data["DetailError/M_SD"]        = self._mergeSD(Data["DetailError/M_SD"], Data["DetailError/M_MAE"], N)
    Data["DetailError/M_MAE"]       = self._mergeMean(Data["DetailError/M_MAE"], N)
    Data["DetailError/R_SD"]        = self._mergeSD(Data["DetailError/R_SD"], Data["DetailError/R_MAE"], N)
    Data["DetailError/R_MAE"]       = self._mergeMean(Data["DetailError/R_MAE"], N)
    Data["DetailError/DistL_SD"]    = self._mergeSD(Data["DetailError/DistL_SD"], Data["DetailError/DistL_MAE"], N)
    Data["DetailError/DistL_MAE"]   = self._mergeMean(Data["DetailError/DistL_MAE"], N)
    Data["DetailError/DistR_SD"]    = self._mergeSD(Data["DetailError/DistR_SD"], Data["DetailError/DistR_MAE"], N)
    Data["DetailError/DistR_MAE"]   = self._mergeMean(Data["DetailError/DistR_MAE"], N)

    return Data


  def _mergeMean(self, Data, N):
    Sum = 0
    for Date in Data:
      Sum += Date

    return Sum/N


  def _mergeSD(self, SDs, Means, N):
    SDSum = 0
    MeanSum = 0

    for i in range(N):
      #print("SD[{}] = {}, Mean[{}] = {}".format(i, SDs[i], i, Means[i]))
      SDSum   += SDs[i]*SDs[i] + Means[i]*Means[i]
      MeanSum += Means[i]

    Mean = MeanSum/N
    Var  = SDSum/N - Mean*Mean

    #print("SD: {}".format(math.sqrt(Var)))

    return math.sqrt(Var)
