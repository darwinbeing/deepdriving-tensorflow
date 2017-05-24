import dd.drive_controller as dddc
import dd

Control = dd.Control_t()
Indicators = dd.Indicators_t()

Indicators.Speed = 0;
DriveController1 = dddc.CDriveController(1)
DriveController1.control(Indicators, Control)
print(Control)

Indicators.Speed = 40;
Indicators.Angle = -1;
DriveController2 = dddc.CDriveController(2)
DriveController2.control(Indicators, Control)
print(Control)

Indicators.Speed = 0;
Indicators.Angle = +1;
DriveController3 = dddc.CDriveController(3)
DriveController3.control(Indicators, Control)
print(Control)