import json
import pickle
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer #reduz palavras diferentes para uma só

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optmizers import SGD

lemmatizer = WordNetLemmatizer() #irá cuidar de lematizar as palavras

padroes = json.load(open("padroes.json").read()) #abrir o arquivo json

palavras = []
classes = []
comandos = []
letras_ignorar = [',', '?', '.', '!']

for comando in padroes["arquivo"]:
    for padrao in comando["padrao"]:
        lista_de_palavras = nltk.word_tokenize(padrao) #pega uma frase e separa ela em uma lista, sendo cada parte da lista uma palavra da frase
        
        for palavra in lista_de_palavras: #adicionar as palavras na lista de palavras
            if palavra not in palavras:
                palavras.append(palavra)

        comandos.append((lista_de_palavras, comando["classe"])) #adicionar em comandos a classe com suas respectivas palavras
        
        classes.append(comando["classe"])

#lematizar as palavras
for i in range(0, len(palavras)):
    if palavras[i] not in letras_ignorar:
        palavras[i] = lemmatizer.lemmatize(palavras[i])

#retirar as palavras duplicasas, se houver alguma
palavras = list(set(palavras))