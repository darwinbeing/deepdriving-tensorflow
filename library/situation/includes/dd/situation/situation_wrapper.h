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
 * @file situation_wrapper.h
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief Wrapper over the situation visualization class.
 *
 */

#ifndef DD_SITUATION_WRAPPER_H
#define DD_SITUATION_WRAPPER_H

// 3rd Party includes
#include <cv.h>

// project includes
#include <dd/common/settings.h>

#ifdef __cplusplus
extern "C"
{
#endif

/// @brief Creates a situation view object.
/// @return Returns the created object.
DLL_API void * CSituationView_create();

/// @brief Destory a situation view object.
/// @param pObject is the object to destory.
DLL_API void CSituationView_destroy(void * pObject);

/// @return Returns the situation image object.
DLL_API uint8_t * CSituationView_getImage(void * pObject);

#ifdef __cplusplus
};
#endif

#endif //DD_SITUATION_WRAPPER_H
