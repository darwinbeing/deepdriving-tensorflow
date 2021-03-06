# Author: Andre Netzeband
# Date: 
#
# This file belongs to the AuDriCa project from the 
# University of Applied Science in Munich.
# This project is derived from the DeepDriving project.
#
# License: MIT
#
# Copyright 2017 Andre Netzeband
#
# Permission is hereby granted, free of charge, to any 
# person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the 
# Software without restriction, including without 
# limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of 
# the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice 
# shall be included in all copies or substantial portions 
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
# OR OTHER DEALINGS IN THE SOFTWARE.
# 

import inspect

class CAssertException(Exception):
  def __init__(self, ErrorText):
    pass

def Assert(Condition, ErrorText = ""):
  if not Condition:
    ContextString = inspect.stack()[1][1] + " (" + str(inspect.stack()[1][2]) + ") "
    raise CAssertException(ContextString + ": " + ErrorText)

def Error():
  ContextString = inspect.stack()[1][1] + " (" + str(inspect.stack()[1][2]) + ") "
  raise CAssertException(ContextString + ": Stopped due to Error")