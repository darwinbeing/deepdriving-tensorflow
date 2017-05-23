import dd.situation_view as ddsv
import cv2

SituationView = ddsv.CSituationView(Size=(320, 500), Background=(0, 1, 0))

cv2.imshow("Image", SituationView.getImage())
cv2.waitKey(0)