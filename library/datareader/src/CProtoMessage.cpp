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
 * @file CProtoMessage.cpp
 * @author Andre Netzeband
 * @date 03.06.2017
 *
 * @brief A class for decoding a caffe protobuffer message.
 * @note All encodings are implemented according to the protobuf-spec: https://developers.google.com/protocol-buffers/docs/encoding
 *
 */

// standard library includes
#include <assert.h>
#include <cstring>

// project includes
#include <dd/datareader/CProtoMessage.h>

namespace dd
{
namespace datareader
{

CProtoMessage::CProtoMessage(std::string const &rString) :
    mChannels(0),
    mWidth(0),
    mHeight(0),
    mpImage(NULL),
    mLabel(0),
    mIsImageEncoded(false)
{
  mFloats.clear();

  parse((uint8_t const *)rString.c_str());
}

CProtoMessage::~CProtoMessage()
{
  deleteImage();
}

void CProtoMessage::deleteImage()
{
  if (mpImage != NULL)
  {
    delete(mpImage);
    mpImage = NULL;
  }
}

static uint8_t const * decodeVarInt(uint8_t const * pMsg, uint64_t &rValue)
{
  uint8_t const * pCurrent = pMsg;
  bool IsLastByte = false;
  bool IsSignExtensionNeeded = false;
  int ContentBit = 0;
  rValue = 0;

  do
  {
    assert(ContentBit <= (64-7));
    // It is the last byte, if the MSB of this byte is not set
    IsLastByte = (*pCurrent & 0x80) == 0;

    // The content is the remaining 7 bits of this byte
    uint8_t Content = (*pCurrent & 0x7F);

    rValue |= (Content << ContentBit);

    // Is bit 7 set, it is a negative number.
    IsSignExtensionNeeded = (Content >> 6) == 1;

    ContentBit += 7;
    pCurrent++;
  } while(!IsLastByte);

  if (IsSignExtensionNeeded)
  {
    for (int i = ContentBit; i < 64; i++)
    {
      rValue |= ((uint64_t)1 << i);
    }
  }

  return pCurrent;
}

static uint8_t const * parseFieldInfo(uint8_t const * pMsg, uint32_t &rFieldNumber, uint32_t &rFieldType)
{
  rFieldNumber = 0;
  rFieldType   = 0;

  uint64_t Value;
  uint8_t const * pCurrent = decodeVarInt(pMsg, Value);

  // the last 3 bits are the type indicator
  rFieldType = Value & 0x00000007;

  // the remaining bits are the type number
  rFieldNumber = (uint32_t)(Value >> 3);

  return pCurrent;
}

void CProtoMessage::parse(uint8_t const * pMsg)
{
  uint8_t const * pCurrent = pMsg;
  bool IsEnd = false;

  while (!IsEnd && *pCurrent != '\0')
  {
    uint32_t Number;
    uint32_t Type;
    pCurrent = parseFieldInfo(pCurrent, Number, Type);

    //printf("Parse field number %d with type %d\n", Number, Type);

    switch(Number)
    {
      case 1:
        pCurrent = parseVarIntUInt32Value(pCurrent, Type, mChannels);
        break;

      case 2:
        pCurrent = parseVarIntUInt32Value(pCurrent, Type, mHeight);
        break;

      case 3:
        pCurrent = parseVarIntUInt32Value(pCurrent, Type, mWidth);
        break;

      case 4:
        deleteImage();
        pCurrent = parseVariableBytes(pCurrent, Type, &mpImage);
        break;

      case 5:
        pCurrent = parseVarIntUInt32Value(pCurrent, Type, mLabel);
        break;

      case 6:
      {
        float Value;
        pCurrent = parseFloatValue(pCurrent, Type, Value);
        mFloats.push_back(Value);
        break;
      }

      case 7:
      {
        uint32_t Value;
        pCurrent = parseVarIntUInt32Value(pCurrent, Type, Value);
        mIsImageEncoded = Value > 0;
        break;
      }

      default:
        printf("Unknown filed number: %d with type %d\n", Number, Type);
        IsEnd = true;
        break;
    }
  }
}

uint8_t const * CProtoMessage::parseVarIntUInt32Value(uint8_t const * pMsg, uint32_t Type, uint32_t &rValue)
{
  if (Type == 0)
  {
    uint64_t Value;
    pMsg = decodeVarInt(pMsg, Value);
    rValue = (uint32_t)Value;
  }
  else
  {
    printf("[Error] Value field must be of type Varint (0) but it is type %d. Cannot parse value field!\n", Type);
  }

  return pMsg;
}

uint8_t const * CProtoMessage::parseVariableBytes(uint8_t const * pMsg, uint32_t Type, uint8_t ** ppBytes)
{
  assert(*ppBytes == NULL);

  if (Type == 2)
  {
    uint64_t Length;
    pMsg = decodeVarInt(pMsg, Length);

    *ppBytes = new uint8_t[Length];

    memcpy(*ppBytes, pMsg, (size_t)Length);

    pMsg += Length;
  }
  else
  {
    printf("[Error] Variable list of bytes must be of type 2. But type %d was readed. Cannot parse byte-list!\n", Type);
  }

  return pMsg;
}

uint8_t const * CProtoMessage::parseFloatValue(uint8_t const * pMsg, uint32_t Type, float &rValue)
{
  if (Type == 5)
  {
    uint32_t RawValue = 0;

    for(int i = 0; i < 4; i++, pMsg++)
    {
      uint8_t const Byte = *pMsg;
      RawValue |= (Byte << (i*8));
    }

    memcpy(&rValue, &RawValue, 4);
  }
  else
  {
    printf("[Error] A float value must be of type 5. But type %d was readed. Cannot parse float-value!\n", Type);
  }

  return pMsg;
}

}
}
