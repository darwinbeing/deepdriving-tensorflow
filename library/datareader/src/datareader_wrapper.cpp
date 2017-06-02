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
 * @file datareader_wrapper.cpp.cpp
 * @author Andre Netzeband
 * @date 02.06.2017
 *
 * @brief Reads the original deepdriving training data.
 *
 */

// standard library includes
#include <stdio.h>
#include <assert.h>

// project includes
#include <dd/datareader/datareader_wrapper.h>
#include <dd/datareader/CDataReader.h>

using namespace dd::datareader;

#ifdef __cplusplus
extern "C"
{
#endif

DLL_API void * CDataReader_create(char * pPath)
{
  return new CDataReader(pPath);
}

DLL_API void CDataReader_destroy(void * pObject)
{
  assert(pObject);
  delete((CDataReader*)pObject);
}

DLL_API uint64_t CDataReader_getFirstKey(void const * pObject)
{
  assert(pObject);
  return ((CDataReader const *)pObject)->getFirstKey();
}

DLL_API uint64_t CDataReader_getLastKey(void const * pObject)
{
  assert(pObject);
  return ((CDataReader const *)pObject)->getLastKey();
}

DLL_API void * CDataReader_createCursor(void * pObject)
{
  assert(pObject);
  return ((CDataReader *)pObject)->createCursor();
}



DLL_API void CDataEntry_destroy(void * pObject)
{
  assert(pObject);
  delete((CDataEntry *)pObject);
}

DLL_API uint64_t CDataEntry_getKey(void const * pObject)
{
  return 0;
}

DLL_API uint32_t CDataEntry_getImageWidth(void const * pObject)
{
  return 0;
}

DLL_API uint32_t CDataEntry_getImageHieght(void const * pObject)
{
  return 0;
}

DLL_API void CDataEntry_getLabels(void const * pObject, Labels_t * pLabel)
{
  return;
}

DLL_API void CDataEntry_getImage(void const * pObject, uint8_t * pImage)
{
  return;
}


#ifdef __cplusplus
};
#endif


