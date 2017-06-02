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
 * @file datareader_wrapper.h
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief The datareader module, which reads the original deepdriving data.
 *
 */

#ifndef DD_DATAREADER_WRAPPER_H
#define DD_DATAREADER_WRAPPER_H

// standard library includes
#include <stdint.h>

// project includes
#include <dd/common/settings.h>
#include <dd/common/datatypes.h>

#ifdef __cplusplus
extern "C"
{
#endif

/// @brief Creates a datareader object.
/// @param pPath Is the path of the data to read.
/// @return Returns the created object.
DLL_API void * CDataReader_create(char * pPath);

/// @brief Destory a datareader object.
/// @param pObject     Is the object to destroy.
DLL_API void CDataReader_destroy(void * pObject);

/// @return Returns the first key of the database.
DLL_API uint64_t CDataReader_getFirstKey(void const * pObject);

/// @return Returns the last key of the database.
DLL_API uint64_t CDataReader_getLastKey(void const * pObject);

/// @return Returns a new cursor to the data of the database.
DLL_API void * CDataReader_createCursor(void * pObject);


/// @brief Destroy a cursor object.
/// @param pObject Is the cursor object to destroy.
DLL_API void CDataEntry_destroy(void * pObject);

/// @return Returns the key of the entry.
/// @param pObject Is the cursor object.
DLL_API uint64_t CDataEntry_getKey(void const * pObject);

/// @return Returns the width of the image
/// @param pObject Is the cursor object.
DLL_API uint32_t CDataEntry_getImageWidth(void const * pObject);

/// @return Returns the height of the image
/// @param pObject Is the cursor object.
DLL_API uint32_t CDataEntry_getImageHieght(void const * pObject);

/// @brief Returns the labels of the entry.
/// @param pObject Is the cursor object.
/// @param pLabel  Is the memory for the labels.
DLL_API void CDataEntry_getLabels(void const * pObject, Labels_t * pLabel);

/// @return Returns the image of this entry.
/// @param pObject Is the cursor object.
/// @param pImage  Is the memory of the image.
DLL_API void CDataEntry_getImage(void const * pObject, uint8_t * pImage);

#ifdef __cplusplus
};
#endif

#endif //DD_DATAREADER_WRAPPER_H
