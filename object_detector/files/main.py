from model import AI
import cv2

modelo = AI(pt=True, model_type="yolov8x")

camera_input = 0

classe = 0

while True:
    #mode.predict vai retonar uma lista de dicionário com informações dos objetos predizidos
    predicted_objects = modelo.prediction(camera_input) #predizir os objetos contidos no frame

    for object in predicted_objects:
        if object["classe"] == classe:
            print("TODO")