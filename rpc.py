import cv2
import time
import os
import HandTrackingModule as htm
import random
from time import sleep

wCam, hCam = 648,480
vid = cv2.VideoCapture(0)
vid.set(3, wCam)
vid.set(4, wCam)

folderpath = "HandGestures"
myList = os.listdir(folderpath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)


print(len(overlayList))

pTime = 0

detector = htm.handDetector(detectionCon = 0.75)

tipIds = [4,8,12,16,20]

while(True):
    success, img = vid.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
       # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
 
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
 
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]
        if (totalFingers-1):
            cv2.waitKey(5)
            randomval = random.choice(overlayList)
            img[200:(h+200),0:w] = randomval
        

        if(overlayList[totalFingers - 1].all() == randomval.any()):
            print("Yay")
        else:
            print("Nay")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)