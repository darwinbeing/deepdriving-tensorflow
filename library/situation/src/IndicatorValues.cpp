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
 * @file IndicatorValues.cpp
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Contains maximum and minimum indicator values.
 *
 */

// standard library includes
#define _USE_MATH_DEFINES
#include <math.h>

// project includes
#include <dd/situation/IndicatorValues.h>

Indicators_t const gInvalidIndicators =
    {
        0.0,
        0.0,
        0.0,
        -9.0,
        -5.0,
        5.0,
        9.0,
        90.0,
        90.0,
        90.0,
        -7.0,
        -5.0,
        7.0,
        90.0,
        90.0
    };

Indicators_t const gMaxIndicators =
    {
         90.0,
         1.0,
         M_PI,
        -4.5,
        -0.5,
         3.5,
         7.5,
         60.0,
         60.0,
         60.0,
        -3.0,
         1.2,
         5.0,
         60.0,
         60.0
    };

Indicators_t const gMinIndicators =
    {
        0.0,
        0.0,
       -M_PI,
       -7.5,
       -3.5,
        0.5,
        4.5,
        0.0,
        0.0,
        0.0,
       -5.0,
       -1.2,
        3.0,
        0.0,
        0.0
    };

