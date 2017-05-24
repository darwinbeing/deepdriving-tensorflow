import dd.situation_view as ddsv
import cv2

SituationView = ddsv.CSituationView()

SituationView.Real.Speed = 20;
SituationView.Real.LL = -6;
SituationView.Real.RR =  6;
SituationView.Estimated.LL = -6;
SituationView.Estimated.RR =  6;
SituationView.Real.DistLL = 40;
SituationView.Real.DistMM = 20;
SituationView.Real.DistRR = 30;
SituationView.Estimated.DistLL = 41;
SituationView.Estimated.DistMM = 21;
SituationView.Estimated.DistRR = 31;

while cv2.waitKey(20) != 27:
    SituationView.update(True, True)
    cv2.imshow("Image", SituationView.getImage())

SituationView.Real.Speed = 20;
SituationView.Real.ML = -5;
SituationView.Real.MR =  5;
SituationView.Estimated.ML = -5;
SituationView.Estimated.MR =  5;
SituationView.Real.L = -5;
SituationView.Real.M = -1;
SituationView.Real.R =  3;
SituationView.Estimated.L = -5;
SituationView.Estimated.M = -1;
SituationView.Estimated.R =  3;
SituationView.Real.DistL = 40;
SituationView.Real.DistR = 30;
SituationView.Estimated.DistL = 41;
SituationView.Estimated.DistR = 31;

while cv2.waitKey(20) != 27:
    SituationView.update(True, True)
    cv2.imshow("Image", SituationView.getImage())
