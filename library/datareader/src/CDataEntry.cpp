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
 * @file CDataEntry.cpp
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief This class abstracts a data entry to the database.
 *
 */

// project includes
#include "includes/dd/datareader/CDataEntry.h"

namespace dd
{
namespace datareader
{

CDataEntry::CDataEntry(leveldb::DB * pDB)
{
  mpIterator = NULL;

  assert(pDB);
  leveldb::ReadOptions ReadOptions;
  mpIterator = pDB->NewIterator(ReadOptions);

  if (!mpIterator->status().ok())
  {
    printf("[Error] DB-Error: %s\n", mpIterator->status().ToString().c_str());
    return;
  }

  mpIterator->SeekToFirst();

  if (!mpIterator->Valid() || !mpIterator->status().ok())
  {
    printf("[Error] First entry in database is not valid... maybe Database is empty?\n");
    printf("[Error] DB-Error: %s\n", mpIterator->status().ToString().c_str());
  }

  printf("create cursor...\n");
}

CDataEntry::~CDataEntry()
{
  printf("destroy cursor...\n");

  delete(mpIterator);
  mpIterator = NULL;
}

uint64_t CDataEntry::getKey() const
{
  return 0;
}

uint32_t CDataEntry::getImageWidth() const
{
  return 0;
}

uint32_t CDataEntry::getImageHeight() const
{
  return 0;
}

void CDataEntry::getLabels(Labels_t * pLabels) const
{

}

void CDataEntry::getImage(uint8_t * pImage) const
{

}


}
}