from classes.language import language
from classes.computer_vision import vision
from classes.voice_recognition import voice_recognition

import cv2

import time

import os

import requests

CV = vision(pt=True, model_type="yolov8n")
LANG = language(arquivo=os.path.join(os.getcwd(), "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "arquivos", "models", "model"))
VR = voice_recognition()

LANG.load_files() #carregar os arquivos

tempo_rotacao_360 = 20

camera_index = 1

ip = "172.20.10.8"

voice_index = 1

tempo_nova_acao = 3

numero_rotacoes = 10

camera = cv2.VideoCapture(camera_index)

"""
lagura da tela: 638
considerado centro: [299, 339]
"""

def send_request(string):
    url = f'http://{ip}/{string}'
    
    response = requests.get(url)

    print(f"Mandar a acao {string}")

    print(response)

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

    #camera = cv2.VideoCapture(camera_index)
    
    while (time.time() - tempo_inicial) < tempo:
        _, frame = camera.read()

        results = CV.model.predict(frame, show=True, conf=0.6)[0]

        predicted_objects = objetos_detectados(results)

        encontrada, object = classe_encontrada(predicted_objects, classe)

        if encontrada:
            return True
    
    return False
        
def direction(object):
    #é considerado centro se ele stiver entre 299 e 339
    
    if (object["xc"] >= 180) and (object["xc"] <= 458):
        return "frente"
    
    if (object["xc"] > 458):
        return "dir"
    
    if (object["xc"] < 180):
        return "esque"
    
    return "para"

def nova_acao(classe):
    #camera = cv2.VideoCapture(camera_index)

    tempo_inicial = time.time()

    flag = False

    while (time.time() - tempo_inicial) < tempo_nova_acao:
        _, frame = camera.read()

        results = CV.model.predict(frame, show=True, conf=0.6)[0]

        predicted_objects = objetos_detectados(results)

        encontrada, object = classe_encontrada(predicted_objects, classe) 

        if encontrada:
            flag = True
            break
        
    if not(flag):
        print("nao encontrou nos 3 segundos")

        exit(1)
    
        
    return direction(object)

def objeto_detectado(classe):
    while True:
        _, frame = camera.read()

        results = CV.model.predict(frame, show=True, conf=0.6)[0]

        predicted_objects = objetos_detectados(results)

        encontrada, object = classe_encontrada(predicted_objects, classe) 

        if not(encontrada):
            continue
        else:
            acao = direction(object) #pegar a acao que ele deve fazer

            send_request(acao) #mandar a acao

            if (acao != "frente") or (acao != "para"): #se a acao n for para ir para frente ou parar
                
                time.sleep(1) #nao fazer nada por 1 segundo

                nova_acao_enviada = nova_acao(classe) #pegar a nova acao que ele deve fazer

                send_request(nova_acao_enviada) #mandar a nova acao

                while (nova_acao_enviada != "frente") or (nova_acao_enviada != "para"): #enquanto a nova acao mandada nao for para ir para frente
                    time.sleep(1) #nao fazer nada por 1 segundo

                    nova_acao_enviada = nova_acao(classe) #pegar a nova acao que ele deve fazer

                    send_request(nova_acao_enviada) #mandar a nova acao

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
    frase = VR.vr(voice_index) #pegar a frase por meio do reconhecimento de voz 

    print(f"Frase dita: {frase}")
    
    classe = LANG.get_classe(frase) #predizir a classe
    
    print(f"Classe predizida: {classe}")

    classe = classe_to_index(classe)

    encontrada = try_to_find_class(5, classe) #tenta encontrar a classe durante 5 segundos

    if encontrada: 
        objeto_detectado(classe) #se ecnontrar chama a função de objeto detectado
    else:
        rotacoes = 0

        while (rotacoes <= numero_rotacoes):
            send_request("dir")

            time.sleep(1)

            encontrada = try_to_find_class(3)

            if encontrada:
                objeto_detectado(classe)
            else:
                rotacoes += 1

main()
