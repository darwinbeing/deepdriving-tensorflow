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
#include <dd/situation/datatypes.h>

#ifdef __cplusplus
extern "C"
{
#endif

/// @brief Creates a situation view object.
/// @param Size       Is the size of the situation view.
/// @param Color      Is the background-color of the situation view.
/// @param pImagePath Is the path where the images can be found.
/// @return Returns the created object.
DLL_API void * CSituationView_create(Size_t Size, Color_t Color, char * pImagePath);

/// @brief Destory a situation view object.
/// @param pObject     Is the object to destory.
DLL_API void CSituationView_destroy(void * pObject);

/// @return Returns the situation image object.
/// @param pObject     The Object of the situation view.
DLL_API uint8_t * CSituationView_getImage(void * pObject);

/// @brief Updates the situation view image.
/// @param pObject     The object to update.
/// @param pReal      Are the real indicators that describe the situation.
/// @param pEstimated Are the estimated indicators that describe the situation.
DLL_API void CSituationView_update(void * pObject, Indicators_t *pReal, Indicators_t *pEstimated);

/// @return Returns the invalid indicators values.
DLL_API Indicators_t const * getInvalidIndicators();

/// @return Returns the max indicator values.
DLL_API Indicators_t const * getMaxIndicators();

/// @return Returns the min indicator values.
DLL_API Indicators_t const * getMinIndicators();

#ifdef __cplusplus
};
#endif

#endif //DD_SITUATION_WRAPPER_H
