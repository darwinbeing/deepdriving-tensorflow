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

from . import struct
from . import dense
from . import activation
from . import conv

Sequence       = struct.CSequence()

# Dense layers
Dense          = dense.CDense(Nodes=None)
Dense_BN_ReLU  = lambda Nodes, Name = "Dense_BN_ReLU": \
  struct.CSequence(Name=Name,
                   Layers=[
                     dense.CDense(Nodes=Nodes).setUseBias(False),
                     dense.CBatchNormalization(),
                     activation.ReLU(),
                   ])
Dropout        = dense.CDropout()

# Convolution layers
Conv2D         = conv.CConv2D(Kernel=None, Filters=None)
Conv2D_BN_ReLU = lambda Kernel, Filters, Stride = 1, Padding = "SAME", Groups = 1, Name = "Conv2D_BN_ReLU": \
  struct.CSequence(Name=Name,
                  Layers=[
                    conv.CConv2D(Kernel=Kernel, Filters=Filters, Stride=Stride, Padding=Padding, Groups=Groups).setUseBias(False),
                    dense.CBatchNormalization(),
                    activation.ReLU(),
                    conv.CLogFeatureMap(),
                  ])
MaxPooling     = conv.CPooling(Window=None, Stride=None, Type="MAX")
AvgPooling     = conv.CPooling(Window=None, Stride=None, Type="AVG")
