/**
 * Attention: The original Drive-Controller was implemented by Chenyi Chen
 * in context of the original DeepDriving project (http://deepdriving.cs.princeton.edu/).
 *
 * The following implementation contains several small adaptions and enhancements necessary
 * for working well with SpeedDreams. However the overall copyright and license is the same
 * as for the original project. Since the original files does not contain any license text, it
 * cannot be added to this file. Thus following license text only applies for the changes and
 * enhancements. Keep this in mind, when using the code in your own project.
 */

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
#include <dd/common/datatypes.h>

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
  addHostCar(Real, Estimated);
  addObstacles(LanePosition, Real, Estimated);
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

void CSituationView::addHostCar(CSituation &rReal, CSituation &rEstimated)
{
  if (rReal.isValid())
  {
    addHostCar(rReal, true);
  }

  if (rEstimated.isValid())
  {
    addHostCar(rEstimated, false);
  }
}

static void getCarBoxFromAngle( float * pP1x, float * pP1y,
                                float * pP2x, float * pP2y,
                                float * pP3x, float * pP3y,
                                float * pP4x, float * pP4y,
                                float Angle)
{
  Angle = -Angle;
  *pP1x = -14 * cos(Angle) + 28 * sin(Angle);
  *pP1y =  14 * sin(Angle) + 28 * cos(Angle);
  *pP2x =  14 * cos(Angle) + 28 * sin(Angle);
  *pP2y = -14 * sin(Angle) + 28 * cos(Angle);
  *pP3x =  14 * cos(Angle) - 28 * sin(Angle);
  *pP3y = -14 * sin(Angle) - 28 * cos(Angle);
  *pP4x = -14 * cos(Angle) - 28 * sin(Angle);
  *pP4y =  14 * sin(Angle) - 28 * cos(Angle);
}

void CSituationView::addHostCar(CSituation &rSituation, bool IsGroundTruth)
{
  float P1x, P1y, P2x, P2y, P3x, P3y, P4x, P4y;
  getCarBoxFromAngle(&P1x, &P1y, &P2x, &P2y, &P3x, &P3y, &P4x, &P4y, (float)rSituation.get()->Angle);

  double const CarPosition = mpSituationImage->size().width / 2.0;
  cv::Point Points[4];

  Points[0].x = (int)(P1x + CarPosition);
  Points[0].y = (int)(P1y + 600);
  Points[1].x = (int)(P2x + CarPosition);
  Points[1].y = (int)(P2y + 600);
  Points[2].x = (int)(P3x + CarPosition);
  Points[2].y = (int)(P3y + 600);
  Points[3].x = (int)(P4x + CarPosition);
  Points[3].y = (int)(P4y + 600);

  if (IsGroundTruth)
  {
    cv::fillConvexPoly(*mpSituationImage, Points, 4, cv::Scalar(0, 0, 255));
  }
  else
  {
    int NumberOfPoints = 4;
    cv::Point const * pPoints = Points;
    cv::polylines(*mpSituationImage, &pPoints, &NumberOfPoints, 1, 1, cv::Scalar(0, 255, 0), 2, CV_AA);
  }
}


void CSituationView::addObstacles(int LanePosition, CSituation &rReal, CSituation &rEstimated)
{
  if (rReal.isValid())
  {
    addObstacles(LanePosition, rReal, true);
  }

  if (rEstimated.isValid())
  {
    addObstacles(LanePosition, rEstimated, false);
  }
}


void CSituationView::addObstacles(int LanePosition, CSituation &rSituation, bool IsGroundTruth)
{
  int const Lanes = rSituation.getNumberOfLanes();

  if (rSituation.isCarInLane())
  {
    if (Lanes == 3 || Lanes == 1)
    {
      if (rSituation.isLeftLane() && rSituation.isDistLLValid())
      {
        drawObstacle(LanePosition - 50, (int)(rSituation.get()->DistLL*12), IsGroundTruth);
      }

      if (rSituation.isDistMMValid())
      {
        drawObstacle(LanePosition, (int)(rSituation.get()->DistMM*12), IsGroundTruth);
      }

      if (rSituation.isRightLane() && rSituation.isDistRRValid())
      {
        drawObstacle(LanePosition + 50, (int)(rSituation.get()->DistRR*12), IsGroundTruth);
      }
    }
    else if (Lanes == 2)
    {
      if (rSituation.isLeftLane())
      {
        if (rSituation.isDistLLValid())
        {
          drawObstacle(LanePosition - 22, (int)(rSituation.get()->DistLL*12), IsGroundTruth);
        }

        if (rSituation.isDistMMValid())
        {
          drawObstacle(LanePosition + 22, (int)(rSituation.get()->DistMM*12), IsGroundTruth);
        }
      }
      else if (rSituation.isRightLane())
      {
        if (rSituation.isDistRRValid())
        {
          drawObstacle(LanePosition + 22, (int)(rSituation.get()->DistRR*12), IsGroundTruth);
        }

        if (rSituation.isDistMMValid())
        {
          drawObstacle(LanePosition - 22, (int)(rSituation.get()->DistMM*12), IsGroundTruth);
        }
      }

    }
  }
  else if (rSituation.isCarOnLane())
  {
    if (Lanes == 2)
    {
      if (rSituation.isLeftLane() && rSituation.isDistLValid())
      {
        drawObstacle(LanePosition - 22, (int)(rSituation.get()->DistL*12), IsGroundTruth);
      }

      if (rSituation.isRightLane() && rSituation.isDistRValid())
      {
        drawObstacle(LanePosition + 22, (int)(rSituation.get()->DistR*12), IsGroundTruth);
      }
    }
    else
    {
      if (rSituation.isLeftLane() && rSituation.isDistLValid())
      {
        drawObstacle(LanePosition, (int)(rSituation.get()->DistL*12), IsGroundTruth);
      }
      else if (rSituation.isRightLane() && rSituation.isDistRValid())
      {
        drawObstacle(LanePosition, (int)(rSituation.get()->DistR*12), IsGroundTruth);
      }
    }
  }

}

void CSituationView::drawObstacle(int X, int Y, bool Filled)
{
  if (Filled)
  {
    cv::rectangle(*mpSituationImage, cv::Point(X - 14, 600 - Y - 28), cv::Point(X + 14, 600 - Y + 28), cv::Scalar(0, 255, 255), -1);
  }
  else
  {
    cv::rectangle(*mpSituationImage, cv::Point(X - 14, 600 - Y - 28), cv::Point(X + 14, 600 - Y + 28), cv::Scalar(237, 99, 157), 2);
  }
}

}
}
