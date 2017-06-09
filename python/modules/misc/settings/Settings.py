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

import os
import json

class CSettings():
  _Dict = {}
  _Filename = None

  def __init__(self, Filename):
    self._Filename = Filename
    self.load()


  def load(self):
    if not os.path.exists(self._Filename):
      self.store()

    if os.path.exists(self._Filename):
      with open(self._Filename, "r") as File:
        LoadedDict = json.load(File)

      for Key in LoadedDict.keys():
        self._Dict[Key] = LoadedDict[Key]


  def store(self):
    with open(self._Filename, "w") as File:
      json.dump(self._Dict, File, sort_keys=True, indent=2, separators=(',', ': '))


  def __getitem__(self, Key):
    return self._Dict.__getitem__(Key)

  def __setitem__(self, Key, Value):
    self._Dict[Key] = Value

  def __delitem__(self, Key):
    del self._Dict[Key]

  def __iter__(self):
    return iter(self._Dict)

  def __str__(self):
    return json.dumps(self._Dict, sort_keys=True, indent=2, separators=(',', ': '))+"\n"