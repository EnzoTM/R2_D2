from ultralytics import YOLO
import os

class vision:
    #por padrao, training vai ser falso
    def __init__(self, path=None, config_folder="data_set_config.yaml", training=False, model_type="yolov8n", epochs=100, pt=False):
        if (path == None) and not(training) and not(pt):
            print("Erro!")

            raise TypeError

        self.model_type = model_type #qual é o tipo do modelo yolo q vamos usar como base
        self.data_set_configuration_path = os.path.join(os.getcwd(), config_folder)  #arquivo .yaml com as configurações do data_set
        self.epochs = epochs #quantidade de epochs a serem utilizadas
        
        if path != None: #carregar o modelo se algum for dado
            self.model_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "files", "runs", "detect", path, "weights", "last.pt") #pegar o path do modelo ja treinado
            self.model = YOLO(self.model_path)#carregar o modelo ja treinado
        
        if pt: #carregar o mdeolo pretreinado baseado no tipo do medelo
            path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector/model",  self.model_type + ".pt")
            self.model = YOLO(path)


        #se traning for verdadeiro, treinar o modelo
        if training:
            self.train()

            print("Sucesso!")   
    
    def train(self):
        model = YOLO(self.model_type + ".yaml") #criar um novo modelo
        model = YOLO(self.model_type + ".pt") #carregar o modelo pré-treinado
        model = YOLO(self.model_type + ".yaml").load(self.model_type + ".pt") #transferir os pesos do modelo já treinado para o modelo que vamos terinar

        model.train(data=self.data_set_configuration_path, epochs=self.epochs) #treinar o modelo