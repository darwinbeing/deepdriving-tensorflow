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
 * @file settings.h
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief Common settings for the whole project.
 *
 */

#ifndef DD_SETTINGS_H
#define DD_SETTINGS_H

#ifdef COMPILE_DLL
  #define DLL_API __declspec(dllexport)
#else
  #define DLL_API __declspec(dllimport)
#endif

#endif //DD_SETTINGS_H
