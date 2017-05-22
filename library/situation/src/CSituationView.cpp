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

// project includes
#include "includes/dd/situation/CSituationView.h"

namespace dd
{
namespace situation
{

CSituationView::CSituationView():
    mpSituationImage(NULL)
{
  mpSituationImage = new cv::Mat(320, 500, CV_8UC3, cv::Scalar(0, 255, 0));
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

}
}
