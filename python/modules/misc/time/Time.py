def getStringFromTime(Seconds):
  Days = int(Seconds/(3600*24))
  Secons = Seconds - Days*3600*24
  Hours = int(Seconds/3600)
  Seconds = Seconds - Hours*3600
  Minutes = int(Seconds/60)
  Seconds = Seconds - Minutes*60

  String = ""
  if Days > 0:
    String += "{} days, ".format(Days)
  String += "{}:{}:{}".format(Hours, Minutes, Seconds)

  return String