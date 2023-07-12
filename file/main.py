from classes.language import language
from classes.computer_vision import vision
from classes.voice_recognition import voice_recognition

import time

import os

CV = vision(pt=True, model_type="yolov8n")
LANG = language(arquivo=os.path.join(os.getcwd(), "file", "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "file", "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "file", "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "file", "arquivos", "models", "model"))
VR = voice_recognition()

LANG.load_files() #carregar os arquivos

tempo_rotacao_360 = 20

"""
2 --> frente
1 --> esquerda
3 --> direita
-1 --> erro

lagura da tela: 638
considerado centro: [299, 339]
"""

def detectar(classe):
    """
    retorna verdadeiro se encintar o objeto e falso se não encontrar
    """
    detected_objects = [] #lista dos objetos que ele controu

    detected_objects = CV.prediction(0)

    #para cada objeto detectad
    for object in detected_objects:
        #se o objeto for da classe que estamos procurando
        if object["classe"] == classe: 
            print("92387687429462342r4927342764")
            return True #retornar verdadeiro, pois encontrou a classe
    
    return False #retornar falso, pois não encontrou a classe

def objeto_detectado(classe):
    detected_objects = [] #lista dos objetos que ele controu

    while True:
        detected_objects = CV.prediction(0)

        #para cada objeto detectad
        for object in detected_objects:
            #se o objeto for da classe que estamos procurando
            if object["classe"] == classe: 
                #é considerado centro se ele stiver en
                # tre 299 e 339

                print(f"Ta aqui cacete asdkjavsdkoajhvdad: {object['xc']}")
                
                if (object["xc"] >= 299) and (object["xc"] <= 339):
                    return 2
                
                if (object["xc"] > 339):
                    return 3
                
                if (object["xc"] < 299):
                    return 1
                
                return -1

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

    tempo_inicial = time.time() #tempo inicial

    #ele vai tentar encontrar o objeto em um tempo de 5 segundos
    while (time.time() - tempo_inicial) < 5:
        flag = detectar(classe)

        if flag:
            print(f"alskiudfygasuikdfvgsaukdafd9qfvwiertqwueiwqdeq8eity7cqdeqweiygkqiuefwqiyektgqwdeqwtiekgqwewq: {objeto_detectado(classe)}")
            break #significa que achou o objeto


    #se apos 5 segundos flag for falso signifca que ele nao achou o objeto
    if not(flag):
        tempo_inicial = time.time()

        #fazer o robo girar 360 graus para ver se ele acha o objetos nos seus arredores
        while (time.time() - tempo_inicial) < tempo_rotacao_360:
            flag = detectar(classe)

            if flag:
                print(f"alskiudfygasuikdfvgsaukdafd9qfvwiertqwueiwqdeq8eity7cqdeqweiygkqiuefwqiyektgqwdeqwtiekgqwewq: {objeto_detectado(classe)}")
                break
    
    while True:
        flag = detectar(classe)

        if flag:
            print(f"alskiudfygasuikdfvgsaukdafd9qfvwiertqwueiwqdeq8eity7cqdeqweiygkqiuefwqiyektgqwdeqwtiekgqwewq: {objeto_detectado(classe)}")


main()