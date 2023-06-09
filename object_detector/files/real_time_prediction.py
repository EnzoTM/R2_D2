from ultralytics import YOLO    
import os
import cv2

#pegar o diretório do nosso modelo já treinado
model_path = os.path.join("/home/enzo/Desktop/R2_D2/object_detector", "files", "runs", "detect", "train5", "weights", "last.pt")


#carregar o modelo treinado
model = YOLO(model_path)

#pegar o video em tempo real
camera = cv2.VideoCapture(2)

while True:
    #pegar cada frame da camera
    _, frame = camera.read()

    results = model.predict(frame, show=True)[0]

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

        print(centro)

    """
    x1 = 0
    y1 = 0
    x2 = 638
    y2 = 478
    """