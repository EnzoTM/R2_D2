from classes.language import language
from classes.computer_vision import vision
from classes.voice_recognition import voice_recognition

import cv2

import time

import os

import requests

CV = vision(model_type="yolov8n")
LANG = language(arquivo=os.path.join(os.getcwd(), "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "arquivos", "models", "model"))
VR = voice_recognition()

LANG.load_files() #carregar os arquivos


camera_index = 1 #o index da camera que será utilizada

ip = "172.20.10.11" #o ip do ESP-32

voice_index = 1 #o index do microfone que será utilizado

tempo_nova_acao = 3 #tempo no qual ele fica utilizando a visao computacional até retornar uma nova acao

numero_rotacoes = 13 #total de rotações para que o robo de 360 graus

camera = cv2.VideoCapture(camera_index) #setar uma variável que será a nossa camera


classes_to_index = { #o nome de cada classe com seu respectivo index
    "pessoa": 0,
    "carro": 2,
    "gato": 15,
    "cachorro": 16,
    "mochila": 24,
    "guarda-chuva": 35,
    "bolsa": 26,
    "bola": 32,
    "garrafa": 39,
    "garfo": 42,
    "faca": 43,
    "banana": 46,
    "maca": 47,
    "sanduíche": 48,
    "cadeira": 56,
    "sofá": 57,
    "planta-em-vaso": 58,
    "cama": 59,
    "mesa-de-jantar": 60,
    "televisão": 62,
    "laptop": 63,
    "mouse": 64,
    "controle-remoto": 65,
    "teclado": 66,
    "celular": 67,
    "micro-ondas": 68,
    "livro": 73,
    "vaso": 75,
    "tesoura": 76,
    "secador-de-cabelo": 78,
    "escova-de-dentes": 79
}

def send_request(string):
    """
    funcao que dada uma string a manda para o ESP-32
    """
    url = f'http://{ip}/{string}'
    
    response = requests.get(url)

    print(f"Mandar a acao {string}")

    print(response)

    time.sleep(0.2) #para evitar que várias ações sejam mandadas uma atraz da outra instantaneamente

def objetos_detectados(results):
    """
    dado os resultados das predições pegar as informações dos objetos predizidos
    """
    predicted_objects = [] #lista dos objetos que vao ser detectados

    for result in results:
            #pegar somente as partes importantes da coordenada da box
            box_coordenates = result.boxes.data.tolist()[0]

            x1 = box_coordenates[0] #coordenada do X a esquerda da box
            x2 = box_coordenates[2] #coordenada do X a direita da box
            y1 = box_coordenates[1] #coordenada do Y em cima da box
            y2 = box_coordenates[3] #coordenada do Y em baixo da box

            object_dict = { #criar um dicionário com as iformações da box
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2,
                'acuracia': box_coordenates[4],
                'xc': (x1 + x2) / 2, #calcular o X do centro
                'yc': (y1 + y2) / 2, #calcular o Y do centro
                'classe': box_coordenates[5]
            }

            predicted_objects.append(object_dict) #adicionar o diciário a lista de objetos detectados
    
    return predicted_objects #retornar a lista dos dicionários dos objetos predizidos

def classe_encontrada(predicted_objects, classe):
    """
    dado a lista de dicionários dos objetos predizidos e uma classe tentar encontrar se ela está presente nessa lista ou não
    """
    #para cada objeto detectado
    for object in predicted_objects:
        #se o objeto for da classe que estamos procurando
        if object["classe"] == classe: 
            return True, object #retornar verdadeiro e o objeto 

    return False, None #retornar falso, pois não encontramos a classe


def try_to_find_class(tempo, classe):
    """
    essa função recebe como paramentro o tempo na qual ela tentará identificar uma classe e qual classe ela está tentando identificar
    se durante esse tempo estabelicido ela achar a classe é retornado True, se ela não achar após o tempo ela retorna Falso
    """
    tempo_inicial = time.time() #pegar o tempo inicial
    
    while (time.time() - tempo_inicial) < tempo: #ficar rodando o looping durante o tempo estabelecido
        _, frame = camera.read() #ler o framde atual da camera

        results = CV.model.predict(frame, show=True, conf=0.6)[0] #predizir os objetos contidos no frame

        predicted_objects = objetos_detectados(results) #chamar a função para saber quais são os objetos detectados

        encontrada, object = classe_encontrada(predicted_objects, classe) #dado os objetos detectados ver se a classe está entre eles

        if encontrada: #se a classe estiver entre os objetos detectados
            return True #retornar verdadeiro
    
    return False #se o código chegou nesse ponto significa que a classe não foi encontrada, logo devemos retornar Falso
        
def direction(object):
    """
    lagura da tela: 638
    Dado o obejto, ou seja, as coordenadas do objeto retornar qual ação dele fazer baseado na posição do seu centro
    """
    
    if (object["xc"] >= 180) and (object["xc"] <= 458):
        return "frente" #ação para ir para frente
    
    if (object["xc"] > 458):
        return "dir" #ação para virar a direita
    
    if (object["xc"] < 180):
        return "esque" #ação para virar a esquerda
    
    return "para" #o código nao deve chegar aqui, mas se chegar algo deu muito errado ent retornar a ação para ele parar

def nova_acao(classe):
    """
    essa função é chamada quando a ação anterior foi virar a direita ou virar a esquerda
    isso significa que agora a posição do robo foi atualizada em relação a centro da box, logo, a nova ação deve ser calculada com cautela
    """

    tempo_inicial = time.time() #pegar o tempo inicial

    flag = False #setar uma flag para sabermos se em determinado tempo a classe foi encontrada ou nao

    #essa flag serve para se de algum problema no robo e ele virar muito ao ponto de nao conseguir mais enxergar a classe

    while (time.time() - tempo_inicial) < tempo_nova_acao: #ficar rodando um looping até um tempo estabelecido de quanto tempo ele deve ficar olhando para calcular uma nova ação
        _, frame = camera.read() #pegar o frame atual da camera

        results = CV.model.predict(frame, show=True, conf=0.6)[0] #predizir os objetos contidos no frame 

        predicted_objects = objetos_detectados(results) #chamar a função para saber quais são os objetos detectados

        encontrada, object = classe_encontrada(predicted_objects, classe)  #dado os objetos detectados ver se a classe está entre eles

        if encontrada: #se a classe foi encontrada
            flag = True #colocar a flag como True, pois encontramos a classe
            break #sair do looping
        
    if not(flag): #se após o fim do looping a classe não foi encontrada
        print("nao encontrou nos 3 segundos") #printar que ele nao conseguiu mais encontrar a classe (deu ruim)

        exit(1) #acabar com o programa
    
    #se o programa chegou até este ponto significa que a classe foi encontrada
    return direction(object) #retornar qual acao deve ser tomada baseada na cooredenada do objeto que estamos procurando

def objeto_detectado(classe):
    """
    essa função é chamada somente quando se há certeza de que a classe foi detectada
    é passado como parametro a classe
    a partir deste momento essa função será a "nova main" do programa
    """
    while True: #ficar em um looping infinito
        """
        ficamos em um looping infinito, pois o objeto de achar a classe já foi alcançado, logo, o novo objetivo será chegar nele
        """
        _, frame = camera.read() #pegar o frame atual da camera

        results = CV.model.predict(frame, show=True, conf=0.6)[0] #predizir os objetos contidos no frame 

        predicted_objects = objetos_detectados(results) #chamar a função para saber quais são os objetos detectados

        encontrada, object = classe_encontrada(predicted_objects, classe) #dado os objetos detectados ver se a classe está entre eles
        
        """
        a funcao classe encontrada, além de retornar se ela foi ecnontrada ou não retorna o objeto
        Portanto, quando ele rotorna que a classe foi encontrada significa que já temos em mão as coordenadas da box do objeto 
        """

        if not(encontrada): #se a classe nao foi encontrada (dificil) continuar com a visao
            continue
        else: #se a classe for encontrada
            acao = direction(object) #pegar a acao que ele deve fazer

            send_request(acao) #mandar a acao para o ESP-32

            if (acao != "frente") or (acao != "para"): #se a acao n for para ir para frente ou parar
                
                time.sleep(1) #nao fazer nada por 1 segundo

                nova_acao_enviada = nova_acao(classe) #pegar a nova acao que ele deve fazer

                send_request(nova_acao_enviada) #mandar a nova acao

                while (nova_acao_enviada != "frente") or (nova_acao_enviada != "para"): #enquanto a nova acao mandada nao for para ir para frente
                    time.sleep(1) #nao fazer nada por 1 segundo

                    nova_acao_enviada = nova_acao(classe) #pegar a nova acao que ele deve fazer

                    send_request(nova_acao_enviada) #mandar a nova acao


def main():
    frase = VR.vr(voice_index) #pegar a frase por meio do reconhecimento de voz 

    print(f"Frase dita: {frase}")
    
    classe = LANG.get_classe(frase) #predizir a classe

    print(f"Classe predizida: {classe}")

    classe = classes_to_index[classe] #pegar o index da classe

    #7 segundos é escolhido para que de tempo da visao iniciar e ficar funcional 
    encontrada = try_to_find_class(7, classe) #tenta encontrar a classe durante 7 segundos

    if encontrada: #se a classe for encontrada
        objeto_detectado(classe) #chamar a função de objeto detectado
    else: #se a classe nao for encontrada
        rotacoes = 0 #setar um contador para saber quantas rotações ja demos

        while (rotacoes <= numero_rotacoes): #ficar em um looping até que ele faça 360 graus
            """
            ele da 360 graus depois que teve todas as rotações necessáras
            A ideia por traz de dar 360 graus é ficar mandando ele ir para a direita numero_rotacoes vezes
            """

            send_request("dir") #mandar o robo ir para a direita

            time.sleep(1) #dormir por um segundo 
            
            #após dormir por 1 segundo significa que o robo já vai ter feito a sua rotacao

            encontrada = try_to_find_class(3, classe) #tentar encontrar a classe por 3 segundos

            if encontrada: #se a classe for encontrada
                time.sleep(5) #para dar um tempo entre a encontrar e começar a visao novamente demos um sleep de 5 segundos


                objeto_detectado(classe) #chamar a função de objeto detectado
            else: #se ela nao for encontrada
                rotacoes += 1 #aumentar o número de rotações dadas
        
        print("Objeto nao encontrado ;-;") #se o código chegou neste ponto signifca que o objeto não foi encontrado

main()