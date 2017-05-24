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
 * @file CSituation.h
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Contains a class, which interprets the current situations from the raw indicators.
 *
 */

#ifndef DD_CSITUATION_H
#define DD_CSITUATION_H

// project includes
#include <dd/situation/datatypes.h>

class CSituation
{
  public:
    /// @brief Constructor.
    /// @param pIndicators Are the indicators to interpret.
    CSituation(Indicators_t * pIndicators);

    /// @brief Destructor.
    ~CSituation();

    /// @return Returns the indicators.
    Indicators_t const * get() const;

    /// @return Returns the number of lanes.
    int getNumberOfLanes() const;

    /// @return Returns true, if the indicators are valid.
    bool isValid() const;

    /// @return Returns true, if the car is inside a lane (in-lane system).
    bool isCarInLane() const;

    /// @return Returns true, if the car is on a lane marking (on-lane marking system).
    bool isCarOnLane() const;

    /// @return Returns true, if a left lane is available.
    bool isLeftLane() const;

    /// @return Returns true, if a right lane is available.
    bool isRightLane() const;

    /// @brief Returns the width of a lane.
    double getLaneWidth() const;

    /// @return Returns true, if the value DistLL is valid.
    bool isDistLLValid() const;

    /// @return Returns true, if the value DistMM is valid.
    bool isDistMMValid() const;

    /// @return Returns true, if the value DistRR is valid.
    bool isDistRRValid() const;

    /// @return Returns true, if the value DistL is valid.
    bool isDistLValid() const;

    /// @return Returns true, if the value DistR is valid.
    bool isDistRValid() const;

  private:
    Indicators_t * mpIndicators;
};

#endif //DD_CSITUATION_H
