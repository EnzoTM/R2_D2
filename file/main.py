from classes.language import language
from classes.computer_vision import vision
from classes.voice_recognition import voice_recognition

import cv2

import time

import os

CV = vision(pt=True, model_type="yolov8n")
LANG = language(arquivo=os.path.join(os.getcwd(), "file", "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "file", "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "file", "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "file", "arquivos", "models", "model"))
VR = voice_recognition()

LANG.load_files() #carregar os arquivos

tempo_rotacao_360 = 20

camera_index = 1

"""
2 --> frente
1 --> esquerda
3 --> direita
-1 --> erro

lagura da tela: 638
considerado centro: [299, 339]
"""

def objetos_detectados(results):
    predicted_objects = [] #list of predicted objects

    for result in results:
            #format to extract only relevant information from the result
            box_coordenates = result.boxes.data.tolist()[0]

            x1 = box_coordenates[0]
            x2 = box_coordenates[2]
            y1 = box_coordenates[1]
            y2 = box_coordenates[3]

            object_dict = { #create dictionary with information about this object
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2,
                'acuracia': box_coordenates[4],
                'xc': int((x1 + x2) / 2),
                'yc': (y1 + y2) / 2,
                'classe': box_coordenates[5]
            }

            predicted_objects.append(object_dict) #add the dictionary to the list of detected objects in the image]
    
    return predicted_objects

def classe_encontrada(predicted_objects, classe):
    #para cada objeto detectad
    for object in predicted_objects:
        #se o objeto for da classe que estamos procurando
        if object["classe"] == classe: 
            return True, object #retornar verdadeiro, pois encontrou a classe

    return False, None


def try_to_find_class(tempo, classe):
    tempo_inicial = time.time()

    camera = cv2.VideoCapture(camera_index)
    
    while (time.time() - tempo_inicial) < tempo:
        _, frame = camera.read()

        results = CV.model.predict(frame, show=True, conf=0.6)[0]

        predicted_objects = objetos_detectados(results)

        encontrada, object = classe_encontrada(predicted_objects, classe)

        if encontrada:
            return tempo
    
    return False
        
def direction(object):
    #é considerado centro se ele stiver entre 299 e 339
    
    if (object["xc"] >= 299) and (object["xc"] <= 339):
        return 2
    
    if (object["xc"] > 339):
        return 3
    
    if (object["xc"] < 299):
        return 1
    
    return -1

def objeto_detectado(classe):
    camera = cv2.VideoCapture(camera_index)

    while True:
        _, frame = camera.read()

        results = CV.model.predict(frame, show=True, conf=0.6)[0]

        predicted_objects = objetos_detectados(results)

        encontrada, object = classe_encontrada(predicted_objects, classe) 

        if not(encontrada):
            continue
        else:
            acao = direction(object)

            print(f"Mandar a acao {acao}")


def classe_to_index(classe):
    if classe == "pessoa": return 0

    if classe == "carro": return 2

    if classe == "gato": return 15

    if classe == "cachorro": return 16

    if classe == "mochila": return 24

    if classe == "guarda-chuva": return 35

    if classe == "bolsa": return 26

    if classe == "bola": return 32

    if classe == "garrafa": return 39

def main():
    frase = VR.vr() #pegar a frase por meio do reconhecimento de voz 

    classe = LANG.get_classe(frase) #predizir a classe

    classe = classe_to_index(classe)

    if try_to_find_class(5, classe):
        objeto_detectado(classe)
    else:
        print("dar o comando para comecar a virar para a direita")

        flag = try_to_find_class(tempo_rotacao_360, classe)

        print("dar o comando para parar de girar")

        if flag:
            objeto_detectado(classe)
        else:
            print("Objeto nao encontrado ;-;")

main()