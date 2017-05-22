import dd_situation_view as ddsv
import cv2

SituationView = ddsv.CSituationView()

cv2.imshow("Image", SituationView.getImage())
cv2.waitKey(0)