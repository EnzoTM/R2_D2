from ultralytics import YOLO
import os

class vision:
    #por padrao, training vai ser falso
    def __init__(self, model_type="yolov8n"):
        self.model_type = model_type #qual é o tipo do modelo yolo q vamos usar como base
        
        #carregar o mdeolo pretreinado baseado no tipo do medelo
        path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector/model",  self.model_type + ".pt")

        self.model = YOLO(path) #setar o modelo