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
 * @file CDataEntry.h
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief This class abstracts a data entry to the database.
 *
 */

// 3rd Party includes
#include <leveldb/db.h>

// project includes
#include <dd/common/datatypes.h>
#include <dd/datareader/CProtoMessage.h>

#ifndef DD_CDATAENTRY_H
#define DD_CDATAENTRY_H

namespace dd
{
namespace datareader
{

class CDataEntry
{
  public:
    /// @brief Constructor.
    /// @param pDB Is the database of this entry.
    CDataEntry(leveldb::DB *pDB);

    /// @brief Destructor.
    ~CDataEntry();

    /// @return Returns the current key of the cursor.
    uint64_t getKey() const;

    /// @return Returns the image width.
    uint32_t getImageWidth() const;

    /// @return Returns the image height.
    uint32_t getImageHeight() const;

    /// @brief Copies the labels from the cursor to the given struct.
    void getLabels(Labels_t * pLabels) const;

    /// @brief Copies the image from the cursor to the given struct.
    void getImage(uint8_t * pImage) const;

  private:
    void deleteMessage();

    leveldb::Iterator * mpIterator;
    CProtoMessage     * mpMessage;
};

}
}

#endif //DD_CDATAENTRY_H

