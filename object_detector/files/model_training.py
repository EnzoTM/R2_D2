from ultralytics import YOLO
import os

model = YOLO("yolov8n.yaml") #criar um novo modelo

data_set_configuration_path = os.path.join(os.getcwd(), "data_set_config.yaml")

results = model.train(data=data_set_configuration_path, epochs=100) #treinar o modelo