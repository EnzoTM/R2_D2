
from classes.computer_vision import vision

v = vision(pt=True, model_type="yolov8n")

while True:
    v.prediction(1)