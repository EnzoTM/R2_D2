from ultralytics import YOLO

model = YOLO("yolov8n.yaml") #criar um novo modelo

results = model.train(data="data_set_config.yaml", epochs=5) #treinar o modelo