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

import tensorflow as tf
import os
import re


def getInt64Feature(Value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[Value]))

def getFloatFeature(Value):
  return tf.train.Feature(float_list=tf.train.FloatList(value=[Value]))

def getByteFeature(Value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[Value]))

_RECORDS_PER_FILE = 2048

class COutputDB():
  def __init__(self, Path):
    if not os.path.exists(Path):
      print("Create TFRecord database directory: {}".format(Path))
      os.makedirs(Path)

    self._Path = Path
    self._Writer = None


  def __del__(self):
    print("Close database-file.")
    self._Writer.close()
    self._Writer = None

  _Filename = "_dataset.tfrecord"

  def _openNextFile(self, Path):
    if self._Writer != None:
      print("Close database-file.")
      self._Writer.close()
      self._Writer = None

    FileNumber = self._getLastFileNumber(Path)
    if FileNumber == None:
      FileNumber = 0
    else:
      FileNumber += 1

    Filename = os.path.join(Path, "{}".format(str(FileNumber).zfill(6)) + self._Filename )
    print("Open database file {}.".format(Filename))
    self._Writer = tf.python_io.TFRecordWriter(path=Filename)
    self._RecordsInFile = 0


  _FilenameTemplate = re.compile('([0-9]+)'+_Filename)
  def _getLastFileNumber(self, Path):
    LastNumber = None
    for File in os.listdir(Path):
      if self._FilenameTemplate.match(File):
        NumberString = self._FilenameTemplate.search(File).group(1)
        Number = int(NumberString)
        if LastNumber == None:
          LastNumber = Number
        elif LastNumber < Number:
          LastNumber = Number

    return LastNumber


  def store(self, Data):
    if self._Writer == None:
      self._openNextFile(self._Path)

    if self._RecordsInFile >= _RECORDS_PER_FILE:
      self._openNextFile(self._Path)

    self._RecordsInFile += 1

    Features = tf.train.Features(feature={
      # Data for managing the image
      'ImageWidth':    getInt64Feature(Data['Image'].shape[1]),
      'ImageHeight':   getInt64Feature(Data['Image'].shape[0]),
      'ImageChannels': getInt64Feature(Data['Image'].shape[2]),
      'Image':         getByteFeature(Data['Image'].tostring()),

      # Data for managing the different tracks
      'TrackName':     getByteFeature(Data['TrackName'].encode('utf-8')),
      'TrackID':       getInt64Feature(Data['TrackID']),
      'RaceID':        getInt64Feature(Data['RaceID']),
      'FrameNumber':   getInt64Feature(Data['FrameNumber']),

      # Additional data
      'Speed':         getFloatFeature(Data['Speed']),
      'Lanes':         getInt64Feature(Data['Lanes']),

      # Original Labels
      'Angle':         getFloatFeature(Data['Angle']),
      'Fast':          getFloatFeature(Data['Fast']),
      'LL':            getFloatFeature(Data['LL']),
      'ML':            getFloatFeature(Data['ML']),
      'MR':            getFloatFeature(Data['MR']),
      'RR':            getFloatFeature(Data['RR']),
      'DistLL':        getFloatFeature(Data['DistLL']),
      'DistMM':        getFloatFeature(Data['DistMM']),
      'DistRR':        getFloatFeature(Data['DistRR']),
      'L':             getFloatFeature(Data['L']),
      'M':             getFloatFeature(Data['M']),
      'R':             getFloatFeature(Data['R']),
      'DistL':         getFloatFeature(Data['DistL']),
      'DistR':         getFloatFeature(Data['DistR']),
    })

    Record = tf.train.Example(features=Features)
    self._Writer.write(Record.SerializeToString())