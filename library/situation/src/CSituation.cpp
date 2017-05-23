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
 * @file CSituation.cpp
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Implements the situation class.
 *
 */

// project includes
#include <dd/situation/CSituation.h>
#include <dd/situation/IndicatorValues.h>
#include <dd/common/settings.h>

CSituation::CSituation(Indicators_t * pIndicators):
    mpIndicators(pIndicators)
{

}

CSituation::~CSituation()
{

}

Indicators_t const * CSituation::get() const
{
  return mpIndicators;
}

int CSituation::getNumberOfLanes() const
{
  int NumberOfLanes;

  if (isCarInLane())
  {
    NumberOfLanes = 1;
  }
  else
  {
    NumberOfLanes = 0;
  }

  if (isLeftLane())
  {
    NumberOfLanes++;
  }

  if (isRightLane())
  {
    NumberOfLanes++;
  }

  return NumberOfLanes;
}

bool CSituation::isValid() const
{
  return mpIndicators != NULL;
}

bool CSituation::isCarInLane() const
{
  if (!isValid())
  {
    return false;
  }

  return (mpIndicators->ML >= gMinIndicators.ML) && (mpIndicators->ML <= gMaxIndicators.ML) &&
      (mpIndicators->MR >= gMinIndicators.MR) && (mpIndicators->MR <= gMaxIndicators.MR);
}

bool CSituation::isCarOnLane() const
{
  if (!isValid())
  {
    return false;
  }

  return (mpIndicators->M >= gMinIndicators.M) && (mpIndicators->M <= gMaxIndicators.M);
}

bool CSituation::isLeftLane() const
{
  if (isCarInLane())
  {
    return (mpIndicators->LL >= gMinIndicators.LL) && (mpIndicators->LL <= gMaxIndicators.LL);
  }
  else if (isCarOnLane())
  {
    return (mpIndicators->L >= gMinIndicators.L) && (mpIndicators->L <= gMaxIndicators.L);
  }

  return false;
}

bool CSituation::isRightLane() const
{
  if (isCarInLane())
  {
    return (mpIndicators->RR >= gMinIndicators.RR) && (mpIndicators->RR <= gMaxIndicators.RR);
  }
  else if (isCarOnLane())
  {
    return (mpIndicators->R >= gMinIndicators.R) && (mpIndicators->R <= gMaxIndicators.R);
  }

  return false;
}

double CSituation::getLaneWidth() const
{
  return 4.0;
}