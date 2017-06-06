import os
import re
import shutil

SummaryFilter = re.compile("^run_(\d+)$")

def cleanSummary(Dir, KeepSummaries = 10):
  if not os.path.exists(Dir):
    return

  LastSummaryNumber = getLastSummaryNumber(Dir)

  if LastSummaryNumber > 0:
    DeleteUntilNumber = LastSummaryNumber - KeepSummaries
    if DeleteUntilNumber > 0:
      for File in os.listdir(Dir):
        if SummaryFilter.match(File):
          if getSummaryNumber(File) < DeleteUntilNumber:
            print("Delete old summary {}".format(File))
            FullFile = os.path.join(Dir, File)
            try:
              shutil.rmtree(FullFile)
            except:
              print("Cannot delete now...")

def getNextSummaryDir(ParentDir):
  if ParentDir is None:
    return None

  return "run_{}".format(getLastSummaryNumber(ParentDir)+1)

def getLastSummaryDir(ParentDir):
  if ParentDir is None:
    return None

  return "run_{}".format(getLastSummaryNumber(ParentDir))

def getLastSummaryNumber(ParentDir):
  if not os.path.exists(ParentDir):
    return 0

  LastNumber = 0
  for File in os.listdir(ParentDir):
    if SummaryFilter.match(File):
      Number = getSummaryNumber(File)
      if Number > LastNumber:
        LastNumber = Number

  return LastNumber

def getSummaryNumber(File):
  return int(SummaryFilter.search(File).group(1))
