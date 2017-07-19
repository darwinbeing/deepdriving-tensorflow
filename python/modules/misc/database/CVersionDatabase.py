from . import CDatabase

import debug

class CVersionDatabase(CDatabase):
  def __init__(self, Version):
    super().__init__()
    self._Version = Version
    self._UpdateDict = {}
    self._VersionTableName = "__DatabaseInfo"
    self._VersionColumn    = "Version"


  def open(self, File):
    super().open(File)
    self.updateDatabase(self._Version)


  @property
  def Version(self):
    with self as Cursor:
      TableName  = self._VersionTableName
      ColumnName = self._VersionColumn

      Cursor.execute("CREATE TABLE IF NOT EXISTS {tn} ({cn} INTEGER);"
                     .format(tn=TableName, cn=ColumnName))

      Cursor.execute("INSERT INTO {tn}({cn}) SELECT 0 WHERE NOT EXISTS(SELECT 1 FROM {tn});"
                     .format(tn=TableName, cn=ColumnName))

      Cursor.execute("SELECT {cn} FROM {tn};"
                     .format(tn=TableName, cn=ColumnName))

      Rows = Cursor.fetchall()
      debug.Assert(len(Rows) == 1, "Wrong number of rows in DatabaseInfo table ({})!".format(len(Rows)))
      return Rows[0][0]

    return None


  def updateDatabase(self, Version):
    CurrentVersion = self.Version
    debug.Assert(Version >= CurrentVersion, "Requested lowever version of database ({}) than the current one ({})!".format(Version, CurrentVersion))

    if CurrentVersion < Version:
      print("Current database version is {}, requested verson is {}: Perform update...".format(CurrentVersion, Version))

      while Version > CurrentVersion:
        self._updateDatabaseTowardsVersion(CurrentVersion, Version)
        CurrentVersion = self.Version


  def _updateDatabaseTowardsVersion(self, CurrentVersion, Version):
    InitialVersion = CurrentVersion
    FoundFunction = None
    while (FoundFunction is None) and (CurrentVersion <= Version):
      CurrentVersion += 1
      if CurrentVersion in self._UpdateDict:
        FoundFunction = self._UpdateDict[CurrentVersion]

    debug.Assert(FoundFunction is not None, "Cannot find an update function for version {} update!".format(Version))

    print("* Update from Version {} to {}...".format(InitialVersion, CurrentVersion))
    FoundFunction(self)
    self._setVersion(CurrentVersion)


  def addUpdateFunction(self, Version, Function):
    self._UpdateDict[Version] = Function


  def _setVersion(self, NewVersion):
    with self as Cursor:
      TableName  = self._VersionTableName
      ColumnName = self._VersionColumn

      Cursor.execute("UPDATE {tn} SET {cn} = \"{v}\";"
                     .format(tn=TableName, cn=ColumnName, v=NewVersion))
