import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# x is the raw distance y is the value in cm
x = [240, 188, 161, 125, 110, 98, 90, 85, 75, 64, 62, 57, 52, 50, 47, 44, 43]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2) # y = Ax^2 + Bx + c

# Loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=False)

    if hands:
        lmList = hands[0]["lmList"]
        x, y, w, h = hands[0]['bbox']
        x1, y1, _ = lmList[5]
        x2, y2, _ = lmList[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A*distance**2 + B*distance + C

        # print(distanceCM, distance)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 3)
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))

    cv2.imshow("Image", img)
    cv2.waitKey(1)