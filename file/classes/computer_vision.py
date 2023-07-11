from ultralytics import YOLO
import os
import cv2

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

    def prediction(self, camera_input):
        camera = cv2.VideoCapture("DroidCam Source 3", cv2.CAP_DSHOW)
        #self.model.info()
        #camera = cv2.VideoCapture(camera_input) #receber o que a camera está gravando
        _, frame = camera.read() #pegar o frame atual da camera

        predicted_objects = [] #lista de objetos predizidos

        results = self.model.predict(frame, show=True, conf=0.6)[0]

        for result in results:
            #formatar para extrair somente as informações relevantes do resultado
            box_coordenates = result.boxes.data.tolist()[0]

            x1 = box_coordenates[0]
            x2 = box_coordenates[2]
            y1 = box_coordenates[1]
            y2 = box_coordenates[3]

            object_dict = { #criar o dicionário com as informações referente a este objeto
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2,
                'acuracia': box_coordenates[4],
                'xc': (x1 + x2) / 2,
                'yc': (y1 + y2) / 2,
                'classe': box_coordenates[5]
            }

            predicted_objects.append(object_dict) #adicionar o dicionario a lista de objetos detectados no imagen
        
    
        return predicted_objects

    def directions(self, centro):
        #lagura = 638

        if (centro >= 299) and (centro <= 339):
            print("FRENTE")
        return