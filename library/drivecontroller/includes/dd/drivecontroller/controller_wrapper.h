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
 * @file controller_wrapper.h
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief Wrapper over the drive controller class.
 *
 */

#ifndef DD_CONTROLLER_WRAPPER_H
#define DD_CONTROLLER_WRAPPER_H

// project includes
#include <dd/common/settings.h>
#include <dd/common/datatypes.h>

#ifdef __cplusplus
extern "C"
{
#endif

/// @brief Creates a drive controller object.
/// @param Lanes Is the number of lanes.
/// @return Returns the created object.
DLL_API void * CDriveController_create(uint32_t Lanes);

/// @brief Destory a drive controller object.
/// @param pObject     Is the object to destroy.
DLL_API void CDriveController_destroy(void * pObject);

/// @brief Controls the car.
/// @param pObject     Is the drive controller object.
/// @param pIndicators Are the situation indicators.
/// @param pControl    Are the control commands.
DLL_API void CDriveController_control(void * pObject, Indicators_t const * pIndicators, Control_t * pControl);

#ifdef __cplusplus
};
#endif

#endif //DD_CONTROLLER_WRAPPER_H
