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
 * @file CDriveController.cpp
 * @author Andre Netzeband
 * @date 22.05.2017
 *
 * @brief The drive controller class.
 *
 */

// standard library includes
#include <iostream>

// project includes
#include <dd/drivecontroller/CDriveController.h>
#include <dd/common/datatypes.h>

namespace dd
{
namespace drivecontroller
{

CDriveController::CDriveController(int Lanes)
{
  mLanes = Lanes;
  slow_down = 0;
  pre_dist_L = 60;
  pre_dist_R = 60;
  left_clear = 0;
  left_timer = 0;
  right_clear = 0;
  right_timer = 0;
  timer_set = 60;
  lane_change = 0;
  steer_trend = 0;
  steering_record[0] = 0;
  steering_record[1] = 0;
  steering_record[2] = 0;
  steering_record[3] = 0;
  steering_record[4] = 0;
  coe_steer = 1.0;
  center_line = 0;
  pre_ML = 0;
  pre_MR = 0;
  steering_head = 0;
  desired_speed = 0;
}

CDriveController::~CDriveController()
{
}

void CDriveController::control(Indicators_t const &rIndicators, Control_t &rControl)
{
  switch (mLanes)
  {
    case 1:
      controlLane1(rIndicators, rControl);
      break;

    case 2:
      controlLane2(rIndicators, rControl);
      break;

    case 3:
      controlLane3(rIndicators, rControl);
      break;
  }
}

void CDriveController::controlLane1(Indicators_t const &rIndicators, Control_t &rControl)
{
  slow_down=100;

  if (rIndicators.DistMM<15) {
    double v_max=20;
    double c=2.772;
    double d=-0.693;
    slow_down=v_max*(1-exp(-c/v_max*rIndicators.DistMM-d));  // optimal vilcity car-following model
    if (slow_down<0) slow_down=0;
  }

  if (-rIndicators.ML+rIndicators.MR<5.5) {
    coe_steer=1.5;
    center_line=(rIndicators.ML+rIndicators.MR)/2;
    pre_ML=rIndicators.ML;
    pre_MR=rIndicators.MR;
    if (rIndicators.M<1)
      coe_steer=0.4;
  } else {
    if (-pre_ML>pre_MR)
      center_line=(rIndicators.L+rIndicators.M)/2;
    else
      center_line=(rIndicators.R+rIndicators.M)/2;
    coe_steer=0.3;
  }

  static float const road_width = 8.0;
  rControl.Steering = (rIndicators.Angle - center_line/road_width) / 0.541052/coe_steer;   // steering control, "rControl.Steering" [-1,1] is the value sent back to TORCS

  if (coe_steer>1 && rControl.Steering>0.1)   // reshape the steering control curve
    rControl.Steering=rControl.Steering*(2.5*rControl.Steering+0.75);

  steering_record[steering_head]=rControl.Steering;  // update previous steering record
  steering_head++;
  if (steering_head==5) steering_head=0;

  if (rIndicators.Fast==1) desired_speed=20;
  else desired_speed=20-fabs(steering_record[0]+steering_record[1]+steering_record[2]+steering_record[3]+steering_record[4])*4.5;
  if (desired_speed<10) desired_speed=10;

  if (slow_down<desired_speed) desired_speed=slow_down;

  ///////////////////////////// speed control
  if (desired_speed>=rIndicators.Speed) {
    rControl.Accelerating = 0.2*(desired_speed-rIndicators.Speed+1);
    if (rControl.Accelerating>1) rControl.Accelerating=1.0;
    rControl.Breaking = 0.0;
  } else {
    rControl.Breaking = 0.1*(rIndicators.Speed-desired_speed);
    if (rControl.Breaking>1) rControl.Breaking=1.0;
    rControl.Accelerating = 0.0;
  }
  ///////////////////////////// END speed control
}

void CDriveController::controlLane2(Indicators_t const &rIndicators, Control_t &rControl)
{
  float const MaxSpeed      = 22;
  float const MaxCurvySpeed = 17.5;
  slow_down=100;

  if (pre_dist_L<20 && rIndicators.DistLL<20) {   // left lane is occupied or not
    left_clear=0;
    left_timer=0;
  } else left_timer++;

  if (pre_dist_R<20 && rIndicators.DistRR<20) {   // right lane is occupied or not
    right_clear=0;
    right_timer=0;
  } else right_timer++;

  pre_dist_L=rIndicators.DistLL;
  pre_dist_R=rIndicators.DistRR;

  if (left_timer>timer_set) {   // left lane is clear
    left_timer=timer_set;
    left_clear=1;
  }

  if (right_timer>timer_set) {   // right lane is clear
    right_timer=timer_set;
    right_clear=1;
  }

  if (lane_change==0 && rIndicators.DistMM < 25) {   // if current lane is occupied

    steer_trend=steering_record[0]+steering_record[1]+steering_record[2]+steering_record[3]+steering_record[4];   // am I turning or not

    if (rIndicators.LL>-8 && left_clear==1 && steer_trend>=0 && rIndicators.Fast == 1) {   // move to left lane
      lane_change=-2;
      coe_steer=2;
      right_clear=0;
      right_timer=0;
      left_clear=0;
      left_timer=0;
      timer_set=30;
    }

    else if (rIndicators.RR<8 && right_clear==1 && steer_trend<=0 && rIndicators.Fast == 1) {   // move to right lane
      lane_change=2;
      coe_steer=2;
      left_clear=0;
      left_timer=0;
      right_clear=0;
      right_timer=0;
      timer_set=30;
    }
  }

    ///////////////////////////////////////////////// prefer to stay in the right lane
  else if (lane_change==0 && rIndicators.DistMM>=15) {

    steer_trend=steering_record[0]+steering_record[1]+steering_record[2]+steering_record[3]+steering_record[4];  // am I turning or not

    if (rIndicators.LL<-8 && right_clear==1 && steer_trend<=0 && steer_trend>-0.2 && rIndicators.Fast == 1) {  // in left lane, move to right lane
      lane_change=2;
      coe_steer=2;
      right_clear=0;
      right_timer=20;
    }
  }
  ///////////////////////////////////////////////// END prefer to stay in the right lane

  if (rIndicators.DistMM < 25)
  {
    double v_max=MaxSpeed;
    double c=2.772;
    double d=-0.693;
    slow_down=v_max*(1-exp(-c/v_max*(rIndicators.DistMM)-d));  // optimal vilocity car-following model
    if (slow_down<0) slow_down=0;
  }

  if (rIndicators.DistMM < 10)
  {
    slow_down=0;
  }

  ///////////////////////////////////////////////// implement lane changing or car-following
  if (lane_change==0) {
    if (-rIndicators.ML+rIndicators.MR<5.5) {
      coe_steer=1.0;
      center_line=(rIndicators.ML+rIndicators.MR)/2;
      pre_ML=rIndicators.ML;
      pre_MR=rIndicators.MR;
      if ((rIndicators.M < 1) && (rIndicators.M > -1))
        coe_steer=0.4;
    } else {
      if (-pre_ML>pre_MR)
        center_line=(rIndicators.L+rIndicators.M)/2;
      else
        center_line=(rIndicators.R+rIndicators.M)/2;
      coe_steer=0.3;
    }
  }

  else if (lane_change==-2) {
    if (-rIndicators.ML+rIndicators.MR<5.5) {
      center_line=(rIndicators.LL+rIndicators.ML)/2;
      if (rIndicators.L>-5 && (rIndicators.M < 1.5) && (rIndicators.M > -1.5))
      {
        if (-rIndicators.L > 3)
        {
          center_line=(center_line+(rIndicators.L+rIndicators.M)/2)/2;
        }
        else
        {
          coe_steer  = 1;
          if (rIndicators.M < 1.25)
          {
            lane_change = 0;
          }
        }
      }
    } else {
      center_line=(rIndicators.L+rIndicators.M)/2;
      coe_steer=1;
      lane_change=-1;
    }
  }

  else if (lane_change==-1) {
    if (rIndicators.L>-5 && rIndicators.M<1.5) {
      center_line=(rIndicators.L+rIndicators.M)/2;
      if (-rIndicators.ML+rIndicators.MR<5.5)
        center_line=(center_line+(rIndicators.ML+rIndicators.MR)/2)/2;
    } else {
      center_line=(rIndicators.ML+rIndicators.MR)/2;
      lane_change=0;
    }
  }

  else if (lane_change==2) {
    if (-rIndicators.ML+rIndicators.MR<5.5) {
      center_line=(rIndicators.RR+rIndicators.MR)/2;
      if (rIndicators.R<5 && (rIndicators.M < 1.5) && (rIndicators.M > -1.5))
      {
        if (rIndicators.R > 3)
        {
          center_line=(center_line+(rIndicators.R+rIndicators.M)/2)/2;
        }
        else
        {
          coe_steer  = 1;
          if (rIndicators.M > -1.25)
          {
            lane_change = 0;
          }
        }
      }
    } else {
      center_line=(rIndicators.R+rIndicators.M)/2;
      coe_steer=1;
      lane_change=1;
    }
  }

  else if (lane_change==1) {
    if (rIndicators.R<5 && rIndicators.M<1.5) {
      center_line=(rIndicators.R+rIndicators.M)/2;
      if (-rIndicators.ML+rIndicators.MR<5.5)
        center_line=(center_line+(rIndicators.ML+rIndicators.MR)/2)/2;
    } else {
      center_line=(rIndicators.ML+rIndicators.MR)/2;
      lane_change=0;
    }
  }
  ///////////////////////////////////////////////// END implement lane changing or car-following

  static const float road_width = 8.0;
  rControl.Steering = (rIndicators.Angle - center_line/road_width)/coe_steer;

  if (lane_change==0 && coe_steer>1 && rControl.Steering>0.1)   // reshape the steering control curve
    rControl.Steering=rControl.Steering*(2.5*rControl.Steering+0.75);

  steering_record[steering_head]=rControl.Steering;   // update previous steering record
  steering_head++;
  if (steering_head==5) steering_head=0;


  if (rIndicators.Fast==1) desired_speed=MaxSpeed;
  else desired_speed=MaxCurvySpeed-fabs(steering_record[0]+steering_record[1]+steering_record[2]+steering_record[3]+steering_record[4])*4.5; // reduce speed
  if (desired_speed<10) desired_speed=10;

  if (slow_down<desired_speed) desired_speed=slow_down;

  ///////////////////////////// speed control
  if (desired_speed>=rIndicators.Speed) {
    rControl.Accelerating = 0.1*(desired_speed-rIndicators.Speed+1);
    if (rControl.Accelerating>1) rControl.Accelerating=1.0;
    rControl.Breaking = 0.0;
  } else {
    rControl.Breaking = 0.1*(rIndicators.Speed-desired_speed);
    if (rControl.Breaking>1) rControl.Breaking=1.0;
    rControl.Accelerating = 0.0;
  }
  ///////////////////////////// END speed control

  ///// Emergency Break
  if (slow_down < 0.1)
  {
    rControl.Accelerating = 0.0;
    rControl.Breaking     = 1.0;
  }
  /////

}

void CDriveController::controlLane3(Indicators_t const &rIndicators, Control_t &rControl)
{
  slow_down = 100;

  if (pre_dist_L < 20 && rIndicators.DistLL < 20)
  {   // left lane is occupied or not
    left_clear = 0;
    left_timer = 0;
  }
  else left_timer++;

  if (pre_dist_R < 20 && rIndicators.DistRR < 20)
  {   // right lane is occupied or not
    right_clear = 0;
    right_timer = 0;
  }
  else right_timer++;

  pre_dist_L = rIndicators.DistLL;
  pre_dist_R = rIndicators.DistRR;

  if (left_timer > timer_set)
  {  // left lane is clear
    left_timer = timer_set;
    left_clear = 1;
  }

  if (right_timer > timer_set)
  {  // right lane is clear
    right_timer = timer_set;
    right_clear = 1;
  }


  if (lane_change == 0 && rIndicators.DistMM < 15)
  {  // if current lane is occupied

    steer_trend = steering_record[0] + steering_record[1] + steering_record[2] + steering_record[3] + steering_record[4];  // am I turning or not

    if (rIndicators.LL > -8 && left_clear == 1 && steer_trend >= 0 && steer_trend < 0.2)
    {  // move to left lane
      lane_change = -2;
      coe_steer = 6;
      right_clear = 0;
      right_timer = 0;
      left_clear = 0;
      left_timer = 30;
      timer_set = 60;
    }

    else if (rIndicators.RR < 8 && right_clear == 1 && steer_trend <= 0 && steer_trend > -0.2)
    {  // move to right lane
      lane_change = 2;
      coe_steer = 6;
      left_clear = 0;
      left_timer = 0;
      right_clear = 0;
      right_timer = 30;
      timer_set = 60;
    }

    else
    {
      double v_max = 20;
      double c = 2.772;
      double d = -0.693;
      slow_down = v_max * (1 - exp(-c / v_max * rIndicators.DistMM - d));  // optimal velocity car-following model
      if (slow_down < 0) slow_down = 0;
    }
  }

    ///////////////////////////////////////////////// prefer to stay in the central lane
  else if (lane_change == 0 && rIndicators.DistMM >= 15)
  {

    steer_trend = steering_record[0] + steering_record[1] + steering_record[2] + steering_record[3] + steering_record[4];  // am I turning or not

    if (rIndicators.RR > 8 && left_clear == 1 && steer_trend >= 0 && steer_trend < 0.2)
    {  // in right lane, move to central lane
      lane_change = -2;
      coe_steer = 6;
      left_clear = 0;
      left_timer = 30;
    }

    else if (rIndicators.LL < -8 && right_clear == 1 && steer_trend <= 0 && steer_trend > -0.2)
    {  // in left lane, move to central lane
      lane_change = 2;
      coe_steer = 6;
      right_clear = 0;
      right_timer = 30;
    }
  }
  ///////////////////////////////////////////////// END prefer to stay in the central lane

  ///////////////////////////////////////////////// implement lane changing or car-following
  if (lane_change == 0)
  {
    if (-rIndicators.ML + rIndicators.MR < 5.5)
    {
      coe_steer = 1.5;
      center_line = (rIndicators.ML + rIndicators.MR) / 2;
      pre_ML = rIndicators.ML;
      pre_MR = rIndicators.MR;
      if (rIndicators.M < 1)
        coe_steer = 0.4;
    }
    else
    {
      if (-pre_ML > pre_MR)
        center_line = (rIndicators.L + rIndicators.M) / 2;
      else
        center_line = (rIndicators.R + rIndicators.M) / 2;
      coe_steer = 0.3;
    }
  }

  else if (lane_change == -2)
  {
    if (-rIndicators.ML + rIndicators.MR < 5.5)
    {
      center_line = (rIndicators.LL + rIndicators.ML) / 2;
      if (rIndicators.L > -5 && rIndicators.M < 1.5)
        center_line = (center_line + (rIndicators.L + rIndicators.M) / 2) / 2;
    }
    else
    {
      center_line = (rIndicators.L + rIndicators.M) / 2;
      coe_steer = 20;
      lane_change = -1;
    }
  }

  else if (lane_change == -1)
  {
    if (rIndicators.L > -5 && rIndicators.M < 1.5)
    {
      center_line = (rIndicators.L + rIndicators.M) / 2;
      if (-rIndicators.ML + rIndicators.MR < 5.5)
        center_line = (center_line + (rIndicators.ML + rIndicators.MR) / 2) / 2;
    }
    else
    {
      center_line = (rIndicators.ML + rIndicators.MR) / 2;
      lane_change = 0;
    }
  }

  else if (lane_change == 2)
  {
    if (-rIndicators.ML + rIndicators.MR < 5.5)
    {
      center_line = (rIndicators.RR + rIndicators.MR) / 2;
      if (rIndicators.R < 5 && rIndicators.M < 1.5)
        center_line = (center_line + (rIndicators.R + rIndicators.M) / 2) / 2;
    }
    else
    {
      center_line = (rIndicators.R + rIndicators.M) / 2;
      coe_steer = 20;
      lane_change = 1;
    }
  }

  else if (lane_change == 1)
  {
    if (rIndicators.R < 5 && rIndicators.M < 1.5)
    {
      center_line = (rIndicators.R + rIndicators.M) / 2;
      if (-rIndicators.ML + rIndicators.MR < 5.5)
        center_line = (center_line + (rIndicators.ML + rIndicators.MR) / 2) / 2;
    }
    else
    {
      center_line = (rIndicators.ML + rIndicators.MR) / 2;
      lane_change = 0;
    }
  }
  ///////////////////////////////////////////////// END implement lane changing or car-following

  static float const road_width = 8.0;
  rControl.Steering = (rIndicators.Angle - center_line / road_width) / 0.541052 / coe_steer;  // steering control, "rControl.Steering" [-1,1] is the value sent back to TORCS

  if (lane_change == 0 && coe_steer > 1 && rControl.Steering > 0.1)   // reshape the steering control curve
    rControl.Steering = rControl.Steering * (2.5 * rControl.Steering + 0.75);

  steering_record[steering_head] = rControl.Steering;  // update previous steering record
  steering_head++;
  if (steering_head == 5) steering_head = 0;


  if (rIndicators.Fast == 1) desired_speed = 20;
  else desired_speed = 20 - fabs(steering_record[0] + steering_record[1] + steering_record[2] + steering_record[3] + steering_record[4]) * 4.5;
  if (desired_speed < 10) desired_speed = 10;

  if (slow_down < desired_speed) desired_speed = slow_down;

  ///////////////////////////// speed control
  if (desired_speed >= rIndicators.Speed)
  {
    rControl.Accelerating = 0.2 * (desired_speed - rIndicators.Speed + 1);
    if (rControl.Accelerating > 1) rControl.Accelerating = 1.0;
    rControl.Breaking = 0.0;
  }
  else
  {
    rControl.Breaking = 0.1 * (rIndicators.Speed - desired_speed);
    if (rControl.Breaking > 1) rControl.Breaking = 1.0;
    rControl.Accelerating = 0.0;
  }
  ///////////////////////////// END speed control}
}

}
}


