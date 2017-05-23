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
 * @file CSituationView.h
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief The class, that creates a situation view.
 *
 */

#ifndef DD_CSITUATIONVIEW_H
#define DD_CSITUATIONVIEW_H

// 3rd party-libraries includes
#include <opencv2/core/core.hpp>

// project includes
#include <dd/situation/datatypes.h>

namespace dd
{
namespace situation
{

class CSituationView
{
  public:
    /// @brief Constructor.
    /// @param rSize      Is the Size of the Situation View.
    /// @param rColor     Is the Background-Color of the Situation View.
    /// @param pImagePath Is the path of the images.
    CSituationView(Size_t &rSize, Color_t &rColor, char * pImagePath);

    /// @brief Destructor.
    ~CSituationView();

    /// @return Returns the situation image.
    cv::Mat * getImage();

    /// @brief Updates the situation view image.
    /// @param pReal      Are the real indicators that describe the situation.
    /// @param pEstimated Are the estimated indicators that describe the situation.
    void update(Indicators_t *pReal, Indicators_t *pEstimated);

  protected:
    cv::Scalar mBackgroundColor;
    cv::Mat * mpSituationImage;
};

}
}


#endif //DD_CSITUATIONVIEW_H
