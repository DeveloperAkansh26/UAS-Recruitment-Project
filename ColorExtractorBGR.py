import cv2
import numpy as np


path = "resources/1.png"

img = cv2.imread(path)
img = cv2.resize(img, (640, 480))

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", [640, 300])
cv2.createTrackbar("B Min", "TrackBars", 0, 255, lambda x: x)
cv2.createTrackbar("B Max", "TrackBars", 255, 255, lambda x: x)
cv2.createTrackbar("G Min", "TrackBars", 0, 255, lambda x: x)
cv2.createTrackbar("G Max", "TrackBars", 255, 255, lambda x: x)
cv2.createTrackbar("R Min", "TrackBars", 0, 255, lambda x: x)
cv2.createTrackbar("R Max", "TrackBars", 255, 255, lambda x: x)


while True:
    lower = np.array([cv2.getTrackbarPos("B Min", "TrackBars"),
                      cv2.getTrackbarPos("G Min", "TrackBars"),
                      cv2.getTrackbarPos("R Min", "TrackBars")])

    upper = np.array([cv2.getTrackbarPos("B Max", "TrackBars"),
                      cv2.getTrackbarPos("G Max", "TrackBars"),
                      cv2.getTrackbarPos("R Max", "TrackBars")])

    mask = cv2.inRange(img, lower, upper)
    cv2.imshow("Mask", mask)
    cv2.imshow("Original", img)
    cv2.waitKey(1)
