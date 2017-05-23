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
 * @file CSituationView.cpp
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief TODO
 *
 */

// standard library includes
#include <stdio.h>
#include <assert.h>

// 3rd party-libraries
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <dd/situation/datatypes.h>

// project includes
#include "includes/dd/situation/CSituationView.h"

namespace dd
{
namespace situation
{

CSituationView::CSituationView(Size_t &rSize, Color_t &rColor, char * pImagePath):
    mpSituationImage(NULL)
{
  uint8_t const R = (uint8_t)(rColor.R*255.0);
  uint8_t const G = (uint8_t)(rColor.G*255.0);
  uint8_t const B = (uint8_t)(rColor.B*255.0);
  mBackgroundColor = cv::Scalar(B, G, R);

  mpSituationImage = new cv::Mat((int)rSize.Width,
                                 (int)rSize.Height,
                                 CV_8UC3,
                                 mBackgroundColor);
}

CSituationView::~CSituationView()
{
  if (mpSituationImage)
  {
    delete(mpSituationImage);
    mpSituationImage = NULL;
  }
}

cv::Mat * CSituationView::getImage()
{
  assert(mpSituationImage);
  return mpSituationImage;
}

void CSituationView::update(Indicators_t *pReal, Indicators_t *pEstimated)
{
  if (pReal)
  {
    printf("LL: %f\n", pReal->LL);
  }

  if (pEstimated)
  {
    printf("RR: %f\n", pEstimated->RR);
  }
}

}
}
