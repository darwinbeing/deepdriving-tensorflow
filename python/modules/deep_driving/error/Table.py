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

from .Reference import Reference

NameDictSelf = {
  'Angle': 'Angle',
  'Fast': 'Fast',
  'LL': 'LL',
  'ML': 'ML',
  'MR': 'MR',
  'RR': 'RR',
  'DistLL': 'DistLL',
  'DistMM': 'DistMM',
  'DistRR': 'DistRR',
  'L': 'L',
  'M': 'M',
  'R': 'R',
  'DistL': 'DistL',
  'DistR': 'DistR'
}

def getTableHeader(CellWidth):
  ProgressString = "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("Type") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("Angle") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("LL") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("ML") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("MR") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("RR") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("DistLL") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("DistMM") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("DistRR") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("L") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("M") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("R") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("DistL") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("DistR") + "|"
  ProgressString += str("{:^" + str(CellWidth) + "}").format("Fast") + "|"
  return ProgressString


def getTableLine(CellWidth):
  ProgressString = "+"
  for i in range(15):
    ProgressString += str("{:-^" + str(CellWidth) + "}").format("") + "+"
  return ProgressString


def getTableMean(Dict, CellWidth, NameDict = NameDictSelf):
  CellWidth -= 1
  ProgressString = "|"
  ProgressString += str("{:^" + str(CellWidth + 1) + "}").format("MAE") + "|"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['Angle']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['LL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['ML']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['MR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['RR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistLL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistMM']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistRR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['L']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['M']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['R']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['Fast']]) + " |"
  return ProgressString


def getTableMeanRef(Dict, CellWidth, NameDict = NameDictSelf):
  # Reference values taken from:
  # "Extracting Cognition out of Images for the Purpose of Autonomous Driving".
  # PhD Thesis of Chenyi Chen. May 2016.
  CellWidth -= 2
  ProgressString = "|"
  ProgressString += str("{:^" + str(CellWidth + 2) + "}").format("MAE/Ref") + "|"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['Angle']] / Reference['MAE']['Angle']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['LL']] / Reference['MAE']['LL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['ML']] / Reference['MAE']['ML']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['MR']] / Reference['MAE']['MR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['RR']] / Reference['MAE']['RR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistLL']] / Reference['MAE']['DistLL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistMM']] / Reference['MAE']['DistMM']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistRR']] / Reference['MAE']['DistRR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['L']] / Reference['MAE']['L']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['M']] / Reference['MAE']['M']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['R']] / Reference['MAE']['R']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistL']] / Reference['MAE']['DistL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistR']] / Reference['MAE']['DistR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['Fast']] / Reference['MAE']['Fast']) + "% |"
  return ProgressString


def getTableSD(Dict, CellWidth, NameDict = NameDictSelf):
  CellWidth -= 1
  ProgressString = "|"
  ProgressString += str("{:^" + str(CellWidth + 1) + "}").format("SD") + "|"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['Angle']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['LL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['ML']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['MR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['RR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistLL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistMM']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistRR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['L']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['M']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['R']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistL']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['DistR']]) + " |"
  ProgressString += str("{:>" + str(CellWidth) + ".2f}").format(Dict[NameDict['Fast']]) + " |"
  return ProgressString


def getTableSDRef(Dict, CellWidth, NameDict = NameDictSelf):
  # Reference values taken from:
  # "Extracting Cognition out of Images for the Purpose of Autonomous Driving".
  # PhD Thesis of Chenyi Chen. May 2016.
  CellWidth -= 2
  ProgressString = "|"
  ProgressString += str("{:^" + str(CellWidth + 2) + "}").format("SD/Ref") + "|"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['Angle']] / Reference['SD']['Angle']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['LL']] / Reference['SD']['LL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['ML']] / Reference['SD']['ML']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['MR']] / Reference['SD']['MR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['RR']] / Reference['SD']['RR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistLL']] / Reference['SD']['DistLL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistMM']] / Reference['SD']['DistMM']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistRR']] / Reference['SD']['DistRR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['L']] / Reference['SD']['L']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['M']] / Reference['SD']['M']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['R']] / Reference['SD']['R']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistL']] / Reference['SD']['DistL']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['DistR']] / Reference['SD']['DistR']) + "% |"
  ProgressString += str("{:>" + str(CellWidth) + ".1f}").format(
    100 * Dict[NameDict['Fast']] / Reference['SD']['Fast']) + "% |"
  return ProgressString
