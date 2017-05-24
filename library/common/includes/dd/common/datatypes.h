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
 * @file datatypes.h
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Defines datatypes for the situation view.
 *
 */

#ifndef DD_DATATYPES_H
#define DD_DATATYPES_H

/// @brief Defines a color value.
typedef struct
{
  double R;
  double G;
  double B;
} Color_t;

/// @brief Defines a size value.
typedef struct
{
  double Width;
  double Height;
} Size_t;

/// @brief The indicators to describe the near situations.
typedef struct
{
  double Speed;
  double Fast;
  double Angle;
  double LL;
  double ML;
  double MR;
  double RR;
  double DistLL;
  double DistMM;
  double DistRR;
  double L;
  double M;
  double R;
  double DistL;
  double DistR;
} Indicators_t;

#endif //DD_DATATYPES_H
