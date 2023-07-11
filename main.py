from bag_of_words.ai import language
from object_detector.files.computer_vision import vision

import time

CV = vision(pt=True, model_type="yolov8n")
LANG = language()

"""
2 --> frente
1 --> esquerda
3 --> direita
-1 --> erro

lagura da tela: 638
considerado centro: [299, 339]
"""

def detectar():
    """
    retorna verdadeiro se encintar o objeto e falso se não encontrar
    """
    detected_objects = [] #lista dos objetos que ele controu

    detected_objects = CV.prediction(0)

    #para cada objeto detectad
    for object in detected_objects:
        #se o objeto for da classe que estamos procurando
        if object["classe"] == classe: 
            return True #retornar verdadeiro, pois encontrou a classe
    
    return False #retornar falso, pois não encontrou a classe

def alinhar():
    detected_objects = [] #lista dos objetos que ele controu

    detected_objects = CV.prediction(0)

    #para cada objeto detectad
    for object in detected_objects:
        #se o objeto for da classe que estamos procurando
        if object["classe"] == classe: 
            #é considerado centro se ele stiver entre 299 e 339
            
            if (object["xc"] >= 299) or (object["xc"] <= 339):
                return 2
            
            if (object["xc"] > 339):
                return 3
            
            if (object["xc"] < 299):
                return 1
            
            return -1


tempo_rotacao_360 = 20

frase = "ausdajsdfasd" #pegar a frase

classe = LANG.get_classe(frase) #por meio da frase predizir qual é a classe

tempo_inicial = time.time() #tempo inicial

#ele vai tentar encontrar o objeto em um tempo de 5 segundos
while (time.time() - tempo_inicial) < 5:
    flag = detectar()

    if flag:
        break #significa que achou o objeto


#se apos 5 segundos flag for falso signifca que ele nao achou o objeto
if not(flag):
    tempo_inicial = time.time()

    #fazer o robo girar 360 graus para ver se ele acha o objetos nos seus arredores
    while (time.time() - tempo_inicial) < tempo_rotacao_360:
        flag = detectar()

        if flag:
            break

if not(flag):
    print("objeto nao detectado")
else:
    alinhar()