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

class CLayer():
  """
  This is the base class for every layer used in this framework.

  Every layer must contain at minimum the following methods:
   - copy:     Creates a copy of this layer
   - __call__: Creates a copy of this layer, but applies settings from the constructor to the copy.
   - apply:    Applies the layer to a signal.

  Furthermore the following rules are important:
   - Every setter-method of a layer must always return the layers instance
   - Every add/create-method of a layer must return the added or created instance

  """

  def copy(self):
    "This method creates a full copy of the layer, including sub-layers."
    raise Exception("This method must be overwritten: It must create a full copy of this layer.")
    return CLayer()

  def __call__(self):
    "This method creates a full copy of the layer and applies the same settings to the copy like the constructor."
    raise Exception("This method must be overwritten: It must create a full copy of this layer and"
                    "apply the same settings to this copy like for the constructor.")
    return CLayer()

  def apply(self, Input):
    "This method applies a layer to a signal."
    raise Exception("This method must be overwritten: It applies a layer to a input-signal and outputs"
                    "a output ignal.")
    return Input