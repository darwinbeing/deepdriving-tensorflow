import dd.situation_view as ddsv
import cv2

SituationView = ddsv.CSituationView(Size=(320, 660), Background=(0.161, 0.392, 0.008))

SituationView.Real.Speed = 20;
SituationView.Real.LL = -6;
SituationView.Real.RR =  6;
SituationView.update(True, True)

while cv2.waitKey(20) != 27:
    SituationView.update(True, True)
    cv2.imshow("Image", SituationView.getImage())
