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
 * @file CDataReader.h
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief A class for reading leveldb treining data for deepdriving.
 *
 */

// 3rd Party includes
#include <leveldb/db.h>

// project includes
#include <dd/datareader/CDataEntry.h>
#include <dd/common/datatypes.h>

#ifndef DD_CDATAREADER_H
#define DD_CDATAREADER_H

namespace dd
{
namespace datareader
{

class CDataReader
{
  public:
    /// @brief Constructor.
    /// @param pPath Is the path where the data is stored.
    CDataReader(char const * pPath);

    /// @brief Destructor.
    ~CDataReader();

    /// @return Returns the first key.
    uint64_t getFirstKey() const { return mFirstKey; }

    /// @return Returns the last key.
    uint64_t getLastKey()  const { return mLastKey; }

    /// @return Creates a new cursor to the data of the database.
    CDataEntry * createCursor();

  private:
    void readDBStatus();

    leveldb::DB * mpDB;
    uint64_t      mLastKey;
    uint64_t      mFirstKey;
};

}
}

#endif //DD_CDATAREADER_H
