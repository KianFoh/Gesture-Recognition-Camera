import cv2
import mediapipe as mp
import time
import threading
import os

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

path = 'E:\Projects\Gesture Recognition Camera\Images'
number = 0
cx1 = 0
cy1 = 0
cx2 = 0
cy2 = 0
counter = 0
number_pic = 0

def Capture():
    global counter
    counter = 3
    for _ in range(3):
        time.sleep(1)
        counter -= 1
    time.sleep(0.2)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    cv2.imwrite(os.path.join(path, timestr+".png"), image)

t = threading.Thread(target=Capture)
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if counter != 0:
        cv2.putText(image, f'Capture in: {counter}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                    3, (0, 255, 0), 3)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape

                if id == 4:
                    cx1, cy1 = int(lm.x * w), int(lm.y * h)
                    #cv2.circle(image, (cx1, cy1), 10, (255, 0, 255), cv2.FILLED)
                elif id == 8:
                    cx2, cy2 = int(lm.x * w), int(lm.y * h)
                    #cv2.circle(image, (cx2, cy2), 10, (255, 0, 255), cv2.FILLED)

                cdx = abs(cx2-cx1)
                cdy = abs(cy2-cy1)

                if cdx < 25 and cdy < 25:
                    number = number + 1
                    if number > 4 and not t.is_alive():
                        t = threading.Thread(target=Capture)
                        t.start()


                #mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS,
                #                      mpDraw.DrawingSpec(color=(0, 0, 200), thickness=2, circle_radius=2),
                #                      mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))



    cv2.imshow("Output", image)
    cv2.waitKey(1)

    if cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 1:
        break
