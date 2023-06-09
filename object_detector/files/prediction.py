from ultralytics import YOLO    
import os

#pegar o diretório do nosso modelo já treinado
model_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "files", "runs", "detect", "train5", "weights", "last.pt") 

image_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "data", "test", "images")

#carregar o modelo treinado
model = YOLO(model_path)

for image in os.listdir(image_path):
    path = os.path.join(image_path, image)
    model.predict(source=path, show=False, hide_labels=False, line_thickness=2)