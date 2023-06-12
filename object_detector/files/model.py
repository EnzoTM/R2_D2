from ultralytics import YOLO
import os
import cv2

class AI:
    #por padrao, training vai ser falso
    def __init__(self, path=None, config_folder="data_set_config.yaml", training=False, model_type="yolov8n.yaml", epochs=100):
        if (path == None) and not(training):
            print("Erro!")

            raise TypeError

        self.config_folder = config_folder #arquivo .yaml com as configurações do data_set
        self.model_type = model_type #qual é o tipo do modelo yolo q vamos usar como base
        self.epochs = epochs #quantidade de epochs a serem utilizadas
        self.model_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "files", "runs", "detect", path, "weights", "last.pt") #pegar o path do modelo ja treinado
        self.model = YOLO(self.model_path) #carregar o modelo ja treinado

        #se traning for verdadeiro, treinar o modelo
        if training:
            self.train()

            print("Sucesso!")

            return 1    
    
    def train(self):
        model = YOLO(self.model_type) #criar um novo modelo

        data_set_configuration_path = os.path.join(os.getcwd(), self.config_folder)

        model.train(data=data_set_configuration_path, epochs=100) #treinar o modelo

    def prediction(self, camera_input):
        camera = cv2.VideoCapture(camera_input) #ficar recebendo o que a camera está gravando

        #por enquanto fazer essa parte ser um looping infinito
        while True:
            _, frame = camera.read() #pegar o frame atual da camera

            results = self.model.predict(frame, show=True)[0]

            for result in results:
                #formatar para extrair somente as informações relevantes do resultado
                box_coordenates = result.boxes.data.tolist()[0]

                print(result.boxes.data.tolist())

                x1 = box_coordenates[0]
                y1 = box_coordenates[1]
                x2 = box_coordenates[2]
                y2 = box_coordenates[3]
                porcentagem_de_certeza = box_coordenates[4]
                classe = box_coordenates[5]

                #lista que irá conter as corrdenadas do centro da box
                centro = [x1 + (x2 / 2), y1 + (y2 / 2)] #x do centro = x1 + (x2 / 2) e y do centro = y1 + (y2 / 2)

                self.directions(centro)

    def directions(self, centro):
        #lagura = 638

        if (centro[0] >= 618) and (centro[0] <= 658):
            print("FRENTE")
        return

         