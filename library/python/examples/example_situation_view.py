import dd.situation_view as ddsv
import cv2

SituationView = ddsv.CSituationView(Size=(320, 660), Background=(0.161, 0.392, 0.008))

SituationView.update(True, True)

cv2.imshow("Image", SituationView.getImage())
cv2.waitKey(0)