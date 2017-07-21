import sqlite3 as db

import debug
import threading
import urllib
import datetime

class CDatabase():
  def __init__(self):
    self._DB = None
    self._Mutex = threading.Lock()


  def __del__(self):
    self.close()


  def open(self, File):
    if self._DB is not None:
      self.close()

    def stringDecoder(ByteString):
      return self.decode(ByteString.decode("utf-8"))

    print("Connect to database file {}...".format(File))
    self._DB = db.connect(File, check_same_thread=False)
    self._DB.text_factory = stringDecoder

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
    self._Mutex.acquire()
    return self.Cursor


  def __exit__(self, type, value, traceback):
    debug.Assert(self._DB is not None, "database must be opened before requesting a cursor!")
    self._DB.commit()
    self._Mutex.release()


  def encode(self, String):
    String = urllib.parse.quote(str(String), safe=' -_')
    return String


  def encodeDatetime(self, Datetime):
    String = Datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return String


  def decodeDatetime(self, String):
    Datetime = datetime.datetime.strptime("%Y-%m-%d %H:%M:%S.%f", String)
    return Datetime


  def decode(self, String):
    return urllib.parse.unquote(String)
