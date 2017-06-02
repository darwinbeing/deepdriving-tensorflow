/**
 *  Copyright (C) 2017 Andre Netzeband
 * 
 *  This file is part of "DeepDriving for Speed-Dreams".
 *
 *  "DeepDriving for Speed-Dreams" is free software: you can redistribute it 
 *  and/or modify it under the terms of the GNU General Public License as 
 *  published by the Free Software Foundation, either version 3 of the License, 
 *  or (at your option) any later version.
 *
 *  "DeepDriving for Speed-Dreams" is distributed in the hope that it 
 *  will be useful, but WITHOUT ANY WARRANTY; without even the implied 
 *  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
 *  See the GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with "DeepDriving for Speed-Dreams".  
 *  If not, see <http://www.gnu.org/licenses/>.  
 */

/**
 * @file CDataReader.cpp
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief A class for reading leveldb treining data for deepdriving.
 *
 */

/// standard library includes
#include <stdio.h>

// project includes
#include <dd/datareader/CDataReader.h>

namespace dd
{
namespace datareader
{

CDataReader::CDataReader(char const * pPath)
{
  mpDB = NULL;
  mFirstKey = 0;
  mLastKey = 0;

  leveldb::Options DBOptions;
  DBOptions.block_size = 65536;
  DBOptions.write_buffer_size = 268435456;
  DBOptions.max_open_files = 100;
  DBOptions.create_if_missing = false;
  DBOptions.paranoid_checks = true;
  leveldb::Status Status = leveldb::DB::Open(DBOptions, pPath, &mpDB);

  if (!Status.ok())
  {
    printf("[Error] Cannot open database on path %s\n", pPath);
    printf("[Error] DB-Error is: %s\n", Status.ToString().c_str());
    fflush(stdout);
    assert(false);
  }

  assert(mpDB);

  readDBStatus();
}

CDataReader::~CDataReader()
{
  printf("Close database...\n");
  if (mpDB)
  {
    delete mpDB;
    mpDB = NULL;
  }
}

void CDataReader::readDBStatus()
{
  leveldb::ReadOptions ReadOptions;
  leveldb::Iterator * pIterator = mpDB->NewIterator(ReadOptions);

  if (!pIterator->status().ok())
  {
    printf("[Error] DB-Error: %s\n", pIterator->status().ToString().c_str());
  }

  pIterator->SeekToFirst();

  if (pIterator->Valid())
  {
    mFirstKey = std::stoull(pIterator->key().ToString());
  }
  else
  {
    printf("[Error] First entry in database is not valid... maybe Database is empty?\n");
    printf("[Error] DB-Error: %s\n", pIterator->status().ToString().c_str());
  }

  pIterator->SeekToLast();

  if (pIterator->Valid())
  {
    mLastKey = std::stoull(pIterator->key().ToString());
  }
  else
  {
    printf("[Error] Last entry in database is not valid... maybe Database is empty?\n");
    printf("[Error] DB-Error: %s\n", pIterator->status().ToString().c_str());
  }

  delete pIterator;

  printf("Read database status:\n");
  printf(" * FirstKey: %llu\n", mFirstKey);
  printf(" * LastKey: %llu\n", mLastKey);
}

CDataEntry * CDataReader::createCursor()
{
  return new CDataEntry(mpDB);
}

}
}

