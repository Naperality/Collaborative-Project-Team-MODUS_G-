import cv2
from cvzone.FaceDetectionModule import FaceDetector
import numpy as np
import json
import pyfirmata
import os

# Create LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
# Load the trained model
recognizer.read('trainer.yml')

# Initialize user IDs and associated names
id = 0
names = ['None']
with open('names.json', 'r') as fs:
    names = json.load(fs)
    names = list(names.values())

# Video Capture from the default camera (camera index 0)
cap = cv2.VideoCapture(0)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't Access!!!")
    exit()

port = "COM3"
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:9:s') #pin 9 Arduino
servo_pinY = board.get_pin('d:10:s') #pin 10 Arduino

detector = FaceDetector()
servoPos = [90, 90]

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # Get the coordinate
        fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
        pos = [fx, fy]


        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])

        if servoX < 0:
            servoX = 0
        elif servoX > 180:
            servoX = 180
        if servoY < 0:
            servoY = 0
        elif servoY > 180:
            servoY = 180

        servoPos[0] = servoX
        servoPos[1] = servoY

        # Recognize the face using the trained model
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        id, confidence = recognizer.predict(gray)
        # Proba greater than 51
        if confidence > 51:
            try:
                # Recognized face
                name = names[id]
                confidence = "  {0}%".format(round(confidence))
            except IndexError as e:
                name = "Who are you?"
                confidence = "N/A"
        else:
            # Unknown face
            name = "Who are you?"
            confidence = "N/A"

        # Display the recognized name and confidence level on the image
        # Below the face
        #cv2.putText(img, name, (bboxs[0]["bbox"][0] + 5, bboxs[0]["bbox"][1] + bboxs[0]["bbox"][3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # Right side of the face
        #cv2.putText(img, name, (bboxs[0]["bbox"][0] + bboxs[0]["bbox"][2] + 10, bboxs[0]["bbox"][1] + bboxs[0]["bbox"][3] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # Above the face
        cv2.putText(img, name, (bboxs[0]["bbox"][0] + bboxs[0]["bbox"][2] - 180 , bboxs[0]["bbox"][1] - 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, confidence, (bboxs[0]["bbox"][0] + 5, bboxs[0]["bbox"][1] + bboxs[0]["bbox"][3] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)
        
        

        # Draw a circle and lines to track the face
        fy = fy - 200
        cv2.circle(img, (fx, fy), 80, (0, 255, 255), 2)
        cv2.putText(img, str(pos), (fx + 15, fy - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)  # x line
        # cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2)  # y line
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "TARGET LOCKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    else:
        cv2.putText(img, "NO TARGET", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2)


    servo_pinX.write(servoPos[0])
    servo_pinY.write(servoPos[1])


    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # Press Escape to exit the webcam / program
    if cv2.waitKey(1) & 0xFF == 27:
        break

print("\n [INFO] Exiting Program.")
# Release the camera
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()