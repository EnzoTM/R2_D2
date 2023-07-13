from classes.computer_vision import vision

import time

import cv2

cv = vision(pt=True, model_type="yolov8n")


camera = cv2.VideoCapture(1)


def teste():
    camera = cv2.VideoCapture(1)
    
    _, frame = camera.read()

    results = cv.model.predict(frame, show=True, conf=0.6)[0]

while True:
    _, frame = camera.read()

    results = cv.model.predict(frame, show=True, conf=0.6)[0]

    teste()