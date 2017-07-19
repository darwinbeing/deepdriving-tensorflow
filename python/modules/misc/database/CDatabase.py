import sqlite3 as db

import debug

class CDatabase():
  def __init__(self):
    self._DB = None


  def __del__(self):
    self.close()


  def open(self, File):
    if self._DB is not None:
      self.close()

    print("Connect to database file {}...".format(File))
    self._DB = db.connect(File)

    Cursor = self.Cursor
    Cursor.execute('SELECT SQLITE_VERSION()')

    print("SQLite version is {}.".format(Cursor.fetchone()[0]))


  def close(self):
    if self._DB is not None:
      print("Close connection to database...")
      self._DB.close()
      self._DB = None


  @property
  def Cursor(self):
    debug.Assert(self._DB is not None, "database must be opened before requesting a cursor!")
    return self._DB.cursor()


  def __enter__(self):
    return self.Cursor


  def __exit__(self, type, value, traceback):
    debug.Assert(self._DB is not None, "database must be opened before requesting a cursor!")
    self._DB.commit()
