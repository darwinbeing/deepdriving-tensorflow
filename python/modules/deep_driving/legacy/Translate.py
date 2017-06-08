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

def translateLabels(Indicators, Labels):
  Indicators.Speed  = 0
  Indicators.Angle  = Labels.Angle
  Indicators.Fast   = Labels.Fast

  Indicators.LL     = Labels.LL
  if Indicators.LL <= -7.5:
    Indicators.LL = -9

  Indicators.ML     = Labels.ML
  if Indicators.ML <= -3.5:
    Indicators.ML = -5

  Indicators.MR     = Labels.MR
  if Indicators.MR >= 3.5:
    Indicators.MR = 5

  Indicators.RR     = Labels.RR
  if Indicators.RR >= 7.5:
    Indicators.RR = 9

  Indicators.DistLL = Labels.DistLL
  if Indicators.DistLL >= 60:
    Indicators.DistLL = 90

  Indicators.DistMM = Labels.DistMM
  if Indicators.DistMM >= 60:
    Indicators.DistMM = 90

  Indicators.DistRR = Labels.DistRR
  if Indicators.DistRR >= 60:
    Indicators.DistRR = 90

  Indicators.L      = Labels.L
  if Indicators.L <= -5:
    Indicators.L = -7

  Indicators.M      = Labels.M
  if Indicators.M <= -1.2 or Indicators.M >= 1.2:
    Indicators.M = -5

  Indicators.R      = Labels.R
  if Indicators.R >= 5:
    Indicators.R = 7

  Indicators.DistL  = Labels.DistL
  if Indicators.DistL >= 60:
    Indicators.DistL = 90

  Indicators.DistR  = Labels.DistR
  if Indicators.DistR >= 60:
    Indicators.DistR = 90

  return Indicators
