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
 * @file CDriveController.h
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief The drive controller class.
 *
 */

#ifndef DD_CDRIVECONTROLLER_H
#define DD_CDRIVECONTROLLER_H

// project includes
#include <dd/common/datatypes.h>

namespace dd
{
namespace drivecontroller
{

class CDriveController
{
  public:
    /// @brief Constructor.
    CDriveController();

    /// @brief Destructor.
    ~CDriveController();
};

}
}


#endif //DD_CDRIVECONTROLLER_H
