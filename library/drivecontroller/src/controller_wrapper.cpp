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
 * @file controller_wrapper.c
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief Implementation of the drive controller wrapper.
 *
 */

// standard library includes
#include <stdio.h>
#include <stdint.h>
#include <assert.h>

// project includes
#include <dd/drivecontroller/controller_wrapper.h>
#include <dd/drivecontroller/CDriveController.h>

using namespace dd::drivecontroller;

#ifdef __cplusplus
extern "C"
{
#endif

DLL_API void * CDriveController_create()
{
  return new CDriveController();
}

DLL_API void CDriveController_destroy(void * pObject)
{
  assert(pObject);
  delete((CDriveController*)pObject);
}

#ifdef __cplusplus
};
#endif

