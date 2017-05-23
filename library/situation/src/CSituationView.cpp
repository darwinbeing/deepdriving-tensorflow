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
#include <iostream>

// 3rd party-libraries
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>

// project includes
#include <dd/situation/CSituationView.h>
#include <dd/situation/ImageHelpers.h>
#include <dd/situation/CSituation.h>
#include <dd/situation/datatypes.h>

#define LANE1_FILENAME "semantic_1lane.png"
#define LANE2_FILENAME "semantic_2lane.png"
#define LANE3_FILENAME "semantic_3lane.png"
#define LANE_WIDTH (4.0)

namespace dd
{
namespace situation
{

CSituationView::CSituationView(Size_t &rSize, Color_t &rColor, char * pImagePath):
    mpSituationImage(NULL),
    mMarkingHead(0)
{
  uint8_t const R = (uint8_t)(rColor.R*255.0);
  uint8_t const G = (uint8_t)(rColor.G*255.0);
  uint8_t const B = (uint8_t)(rColor.B*255.0);
  mBackgroundColor = cv::Scalar(B, G, R);

  mpSituationImage = new cv::Mat((int)rSize.Height,
                                 (int)rSize.Width,
                                 CV_8UC3,
                                 mBackgroundColor);

  mpLane1 = loadImage(pImagePath, LANE1_FILENAME);
  mpLane2 = loadImage(pImagePath, LANE2_FILENAME);
  mpLane3 = loadImage(pImagePath, LANE3_FILENAME);
}

CSituationView::~CSituationView()
{
  delImage(&mpSituationImage);
  delImage(&mpLane1);
  delImage(&mpLane2);
  delImage(&mpLane3);
}

cv::Mat * CSituationView::getImage()
{
  assert(mpSituationImage);
  return mpSituationImage;
}

void CSituationView::update(Indicators_t *pReal, Indicators_t *pEstimated)
{
  CSituation Real(pReal);
  CSituation Estimated(pEstimated);

  int const Lanes = guessLanes(Real, Estimated);
  createBackground();

  int const LanePosition = getLanePosition(Real, Estimated);
  addLanes(Lanes, LanePosition);
  addLaneMarkings(Lanes, LanePosition, Real);
}

int CSituationView::guessLanes(CSituation &rReal, CSituation &rEstimated)
{
  if (rReal.isValid())
  {
    return rReal.getNumberOfLanes();
  }
  else if (rEstimated.isValid())
  {
    return rEstimated.getNumberOfLanes();
  }

  return 0;
}

void CSituationView::createBackground()
{
  *mpSituationImage = mBackgroundColor;
}

int CSituationView::getLanePosition(CSituation &rReal, CSituation &rEstimated)
{
  if (rReal.isValid())
  {
    return getLanePosition(rReal);
  }
  else if (rEstimated.isValid())
  {
    return getLanePosition(rEstimated);
  }

  return mpSituationImage->size[0];
}

int CSituationView::getLanePosition(CSituation &rSituation)
{
  int const ImageWidth = mpSituationImage->size().width;
  double const StreetWidth = rSituation.getNumberOfLanes() * rSituation.getLaneWidth();
  double CarPosition = 0.0;

  if (rSituation.isCarInLane())
  {
    if (rSituation.isLeftLane())
    {
      CarPosition = StreetWidth / 2 + rSituation.get()->LL;
    }
    else
    {
      CarPosition = StreetWidth / 2 + rSituation.get()->ML;
    }
  }
  else if (rSituation.isCarOnLane())
  {
    if (rSituation.isLeftLane())
    {
      CarPosition = StreetWidth / 2 + rSituation.get()->L;
    }
    else
    {
      CarPosition = StreetWidth / 2 + rSituation.get()->M;
    }
  }
  else
  {
    return -100;
  }

  return (int)((ImageWidth/2.0) + CarPosition*12);
}

void CSituationView::addLanes(int Lanes, int LanePosition)
{
  cv::Mat * pLaneImage = NULL;

  switch(Lanes)
  {
    case 1:
      pLaneImage = mpLane1;
      break;

    case 2:
      pLaneImage = mpLane2;
      break;

    case 3:
      pLaneImage = mpLane3;
      break;
  }

  if (pLaneImage && LanePosition > 0)
  {
    int const LaneTopLeftCorner = LanePosition - (int)(pLaneImage->size().width / 2.0);
    cv::Rect RegionToCopy(LaneTopLeftCorner, 0, pLaneImage->size().width, pLaneImage->size().height);
    cv::Mat TargetImage(*mpSituationImage, RegionToCopy);
    pLaneImage->copyTo(TargetImage);
  }
}

void CSituationView::addLaneMarkings(int Lanes, int LanePosition, CSituation &rSituation)
{
  double const Speed = rSituation.isValid() ? rSituation.get()->Speed : 35.0;

  if (Lanes > 1)
  {
    int Pace = int(Speed * 1.2);
    if (Pace > 50)
    {
      Pace = 50;
    }

    boost::posix_time::ptime CurrentTime(boost::posix_time::microsec_clock::local_time());
    double const Difference = (CurrentTime - mLastTime).total_milliseconds()/1000.0;
    mLastTime = CurrentTime;

    mMarkingHead += Pace;
    if (mMarkingHead > 0)
    {
      mMarkingHead = mMarkingHead - 110;
    }
    else if (mMarkingHead < -110)
    {
      mMarkingHead = mMarkingHead + 110;
    }

    int MarkingStart = mMarkingHead;
    int MarkingEnd   = mMarkingHead+55;

    while (MarkingStart <= 660)
    {
      if (Lanes >= 3)
      {
        int LeftLanePosition  = LanePosition - 25;
        int RightLanePosition = LanePosition + 25;

        cv::line(*mpSituationImage, cv::Point2i(LeftLanePosition,  MarkingStart), cv::Point2i(LeftLanePosition,  MarkingEnd), cv::Scalar(255,255,255), 2);
        cv::line(*mpSituationImage, cv::Point2i(RightLanePosition, MarkingStart), cv::Point2i(RightLanePosition, MarkingEnd), cv::Scalar(255,255,255), 2);
      }
      else
      {
        cv::line(*mpSituationImage, cv::Point2i(LanePosition, MarkingStart), cv::Point2i(LanePosition, MarkingEnd), cv::Scalar(255,255,255), 2);
      }

      MarkingStart = MarkingStart + 110;
      MarkingEnd   = MarkingEnd   + 110;
    }
  }
}


}
}
