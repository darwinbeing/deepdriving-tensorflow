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
#include <boost/date_time/posix_time/posix_time.hpp>

// project includes
#include <dd/common/datatypes.h>
#include <dd/situation/CSituation.h>

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
    /// @param pImage      Is the object where to copy the image to.
    void getImage(uint8_t * pImage);

    /// @brief Updates the situation view image.
    /// @param pReal      Are the real indicators that describe the situation.
    /// @param pEstimated Are the estimated indicators that describe the situation.
    void update(Indicators_t *pReal, Indicators_t *pEstimated);

  protected:
    /// @return Returns the number of lanes.
    /// @param rReal      Is the real situation description.
    /// @param rEstimated Is the estimated situation description.
    int guessLanes(CSituation &rReal, CSituation &rEstimated);

    /// @brief Creates a new empty background image.
    void createBackground();

    /// @brief Calculates the lane position inside the situation view.
    /// @param rReal      Is the real situation description.
    /// @param rEstimated Is the estimated situation description.
    int getLanePosition(CSituation &rReal, CSituation &rEstimated);

    /// @brief Calculates the lane position inside the situation view.
    /// @param rSituation  Is the situation description.
    int getLanePosition(CSituation &rSituation);

    /// @brief Adds the lanes to the image.
    /// @param Lanes        Is the number of lanes.
    /// @param LanePosition Is the position of the lane.
    void addLanes(int Lanes, int LanePosition);

    /// @brief Adds lane markings to the image.
    /// @param Lanes        Is the number of lanes.
    /// @param LanePosition Is the position of the lane.
    /// @param rSituation   Is the real situation, which contains the current speed.
    void addLaneMarkings(int Lanes, int LanePosition, CSituation &rSituation);

    /// @brief Adds a host car to the image.
    /// @param rReal      Is the real situation description.
    /// @param rEstimated Is the estimated situation description.
    void addHostCar(CSituation &rReal, CSituation &rEstimated);

    /// @brief Adds a host car to the image.
    /// @param rSituation    Is the situation description.
    /// @param IsGroundTruth Indicates, if the information belongs to the ground truth or not.
    void addHostCar(CSituation &rSituation, bool IsGroundTruth);

    /// @brief Adds obstacles to the image.
    /// @param LanePosition Is the positon of the lane.
    /// @param rReal        Is the real situation description.
    /// @param rEstimated   Is the estimated situation description.
    void addObstacles(int LanePosition, CSituation &rReal, CSituation &rEstimated);

    /// @brief Adds obstacles to the image.
    /// @param LanePosition  Is the positon of the lane.
    /// @param rSituation    Is the situation description.
    /// @param IsGroundTruth Indicates, if the information belongs to the ground truth or not.
    void addObstacles(int LanePosition, CSituation &rSituation, bool IsGroundTruth);

    /// @brief Draws an obstacle to the image.
    /// @param X      Is the X position of the obstacle.
    /// @param Y      Is the Y position of the obstacle.
    /// @param Filled Indicates if the obstacle should be filled or not.
    void drawObstacle(int X, int Y, bool Filled);

    cv::Scalar               mBackgroundColor;
    cv::Mat                * mpSituationImage;
    cv::Mat                * mpLane1;
    cv::Mat                * mpLane2;
    cv::Mat                * mpLane3;
    int                      mMarkingHead;
    boost::posix_time::ptime mLastTime;
};

}
}


#endif //DD_CSITUATIONVIEW_H
