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
 * @file ImageHelpers.cpp
 * @author Andre Netzeband
 * @date 23.05.2017
 *
 * @brief Implements some image helper methods.
 *
 */

// 3rd party-libraries
#include <boost/filesystem/operations.hpp>
#include <boost/filesystem/path.hpp>

// project includes
#include <dd/situation/ImageHelpers.h>

cv::Mat * loadImage(char * pImagePath, char * pFileName)
{
  using namespace boost::filesystem;

  path const ImagePath(pImagePath);
  path const FileName(pFileName);
  path const FilePath = ImagePath / FileName;

  cv::Mat * pImage = new cv::Mat(cv::imread(FilePath.string().c_str()));

  assert(pImage->data);

  return pImage;
}

void delImage(cv::Mat ** ppImage)
{
  if (*ppImage)
  {
    delete(*ppImage);
    *ppImage = NULL;
  }
}
