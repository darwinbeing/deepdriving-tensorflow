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
 * @file ImageHelpers.h
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Defines some helper methods for images.
 *
 */

#ifndef DD_IMAGEHELPERS_H
#define DD_IMAGEHELPERS_H

// 3rd party-libraries
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>


/// @brief Loads an image from a file.
/// @param pImagePath Is the directory from this file.
/// @param pFileName  Is the name of this file.
/// @return Returns a cv::Mat object.
cv::Mat * loadImage(char const * pImagePath, char const * pFileName);

/// @brief Deletes the memory of a cv::Mat object, if it is defined.
/// @param ppImage Is the image to delete. If this *ppImage is 0, nothing will be deleted. After deletion the *ppImage will be 0.
void delImage(cv::Mat ** ppImage);

#endif //DD_IMAGEHELPERS_H
