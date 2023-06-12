from ultralytics import YOLO
import os
import cv2

class AI:
    #por padrao, training vai ser falso
    def __init__(self, path=None, config_folder="data_set_config.yaml", training=False, model_type="yolov8n", epochs=100):
        if (path == None) and not(training):
            print("Erro!")

            raise TypeError

        self.model_type = model_type #qual é o tipo do modelo yolo q vamos usar como base
        self.data_set_configuration_path = os.path.join(os.getcwd(), config_folder)  #arquivo .yaml com as configurações do data_set
        self.epochs = epochs #quantidade de epochs a serem utilizadas
        
        if path != None:
            self.model_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "files", "runs", "detect", path, "weights", "last.pt") #pegar o path do modelo ja treinado
            self.model = YOLO(self.model_path) #carregar o modelo ja treinado

        #se traning for verdadeiro, treinar o modelo
        if training:
            self.train()

            print("Sucesso!")

            return 1    
    
    def train(self):
        model = YOLO(self.model_type + ".yaml") #criar um novo modelo
        model = YOLO(self.model_type + ".pt") #carregar o modelo pré-treinado
        model = YOLO(self.model_type + ".yaml").load(self.model_type + ".pt") #transferir os pesos do modelo já treinado para o modelo que vamos terinar

        model.train(data=self.data_set_configuration_path, epochs=self.epochs) #treinar o modelo

    def prediction(self, camera_input):
        camera = cv2.VideoCapture(camera_input) #ficar recebendo o que a camera está gravando

        #por enquanto fazer essa parte ser um looping infinito
        while True:
            _, frame = camera.read() #pegar o frame atual da camera

            results = self.model.predict(frame, show=True)[0]

            for result in results:
                #formatar para extrair somente as informações relevantes do resultado
                box_coordenates = result.boxes.data.tolist()[0]

                x1 = box_coordenates[0]
                y1 = box_coordenates[1]
                x2 = box_coordenates[2]
                y2 = box_coordenates[3]
                porcentagem_de_certeza = box_coordenates[4]
                classe = box_coordenates[5]

                x_centro = (x1 + x2) / 2

                self.directions(x_centro)

    def directions(self, centro):
        #lagura = 638

        if (centro >= 299) and (centro <= 339):
            print("FRENTE")
        return