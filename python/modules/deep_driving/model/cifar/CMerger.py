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
      "ClassError/Error": [],
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
    Data["ClassError/Error"]        = self._mergeMean(Data["ClassError/Error"], N)

    return Data


  def _mergeMean(self, Data, N):
    Sum = 0
    for Date in Data:
      Sum += Date

    return Sum/N

