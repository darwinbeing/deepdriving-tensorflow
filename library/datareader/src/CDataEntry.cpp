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
#include <dd/common/datatypes.h>
#include "includes/dd/datareader/CDataEntry.h"

namespace dd
{
namespace datareader
{

CDataEntry::CDataEntry(leveldb::DB * pDB)
{
  mpIterator = NULL;
  mpMessage  = NULL;

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
    return;
  }

  mpMessage = new CProtoMessage(mpIterator->value().ToString());

  if (mpMessage->mChannels != 3)
  {
    printf("[Error] Reading wrong number of channels from message. Expected 3 Channels. Read %d Channels.\n", mpMessage->mChannels);
    return;
  }
}

CDataEntry::~CDataEntry()
{
  deleteMessage();

  delete(mpIterator);
  mpIterator = NULL;
}

void CDataEntry::deleteMessage()
{
  if (mpMessage)
  {
    delete(mpMessage);
    mpMessage = NULL;
  }
}

uint64_t CDataEntry::getKey() const
{
  return std::stoull(mpIterator->key().ToString());
}

uint32_t CDataEntry::getImageWidth() const
{
  return mpMessage->mWidth;
}

uint32_t CDataEntry::getImageHeight() const
{
  return mpMessage->mHeight;
}

void CDataEntry::getLabels(Labels_t * pLabels) const
{
  assert(pLabels);
  if (mpMessage->mFloats.size() == 14)
  {
    pLabels->Angle  = mpMessage->mFloats[0];
    pLabels->L      = mpMessage->mFloats[1];
    pLabels->M      = mpMessage->mFloats[2];
    pLabels->R      = mpMessage->mFloats[3];
    pLabels->DistL  = mpMessage->mFloats[4];
    pLabels->DistR  = mpMessage->mFloats[5];
    pLabels->LL     = mpMessage->mFloats[6];
    pLabels->ML     = mpMessage->mFloats[7];
    pLabels->MR     = mpMessage->mFloats[8];
    pLabels->RR     = mpMessage->mFloats[9];
    pLabels->DistLL = mpMessage->mFloats[10];
    pLabels->DistMM = mpMessage->mFloats[11];
    pLabels->DistRR = mpMessage->mFloats[12];
    pLabels->Fast   = mpMessage->mFloats[13];
  }
  else
  {
    printf("[Error] Was not able to read 14 labels from the protobuf-message. Read only %d labels instead.", (int)mpMessage->mFloats.size());
  }
}

void CDataEntry::getImage(uint8_t * pImage) const
{
  int const Height = getImageHeight();
  int const Width  = getImageWidth();

  for (int y = 0; y < Height; y++)
  {
    for (int x = 0; x < Width; x++)
    {
      pImage[(y*Width + x)*3+0]=mpMessage->mpImage[                 y*Width + x];
      pImage[(y*Width + x)*3+1]=mpMessage->mpImage[Height*Width   + y*Width + x];
      pImage[(y*Width + x)*3+2]=mpMessage->mpImage[Height*Width*2 + y*Width + x];
    }
  }
}

bool CDataEntry::isValid() const
{
  return mpIterator->Valid();
}

bool CDataEntry::next()
{
  mpIterator->Next();

  if (mpIterator->Valid())
  {
    if (!mpIterator->status().ok())
    {
      printf("[Error] Entry in database is not valid... maybe Database is corrupted?\n");
      printf("[Error] DB-Error: %s\n", mpIterator->status().ToString().c_str());
      return false;
    }
    else
    {
      deleteMessage();

      mpMessage = new CProtoMessage(mpIterator->value().ToString());

      if (mpMessage->mChannels != 3)
      {
        printf("[Error] Reading wrong number of channels from message. Expected 3 Channels. Read %d Channels.\n", mpMessage->mChannels);
        return false;
      }
    }
  }

  return mpIterator->Valid();
}


}
}