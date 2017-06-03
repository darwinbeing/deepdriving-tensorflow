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
 * @file CProtoMessage.h
 * @author Andre Netzeband
 * @date 03.06.2017
 *
 * @brief A class for interpreting the caffe protobuffer message.
 *
 */

#ifndef DD_CPROTOMESSAGE_H
#define DD_CPROTOMESSAGE_H

// standard library includes
#include <vector>
#include <string>

namespace dd
{
namespace datareader
{

class CProtoMessage
{
  public:
    CProtoMessage(std::string const &rString);
    ~CProtoMessage();

    int32_t mChannels;
    int32_t mWidth;
    int32_t mHeight;
    uint8_t *mpImage;
    int32_t mLabel;
    std::vector<float> mFloats;
    bool mIsImageEncoded;

  private:
    void parse(uint8_t const * pMsg);
    uint8_t const * parseChannels(uint8_t const * pMsg, uint32_t Type);
};

}
}

#endif //DD_CPROTOMESSAGE_H
