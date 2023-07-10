import json
import pickle
import numpy as np
import random


import nltk
from nltk.stem import WordNetLemmatizer #reduz palavras diferentes para uma só

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

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

#guardar as calsses e palavras em um arquivo
pickle.dump(palavras, open("palavras.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

inputs = []
output = [0] * len(classes)

for comando in comandos:
    bag = []

    #pegar as listas de palavras
    padroes_de_palavras = comando[0]

    for i in range(0, len(padroes_de_palavras)):
        padroes_de_palavras[i] = lemmatizer.lemmatize(padroes_de_palavras[i])
    
    for palavra in palavras:
        if palavra in padroes_de_palavras:
            bag.append(1)
        else:
            bag.append(0)

    output[classes.index(comandos[1])] = 1

    inputs.append([bag, output])

random.shuffle(inputs)
training = np.array(inputs)

training_x = []

training_y = []

for i in range(0, len(training[0])):
    training_x.append(training[0][i])

for i in range(0, len(training[1])):
    training_y.append(training[1][i])

 #cirar o medelo 
    model = Sequential(
        [
            #128 input layers, com o tamanho do numero de palavras, e o a activation funcion como relu
            Dense(128, activation="relu", input_shape=(len(inputs[0]),),), 
            #50% de dropout
            Dropout(0.5),
            #64 hidden layers, com acitivation function como relu
            Dense(64, activation="relu"),
            #50% de dropout
            Dropout(0.5),
            #x outptus layers, onde x = numero de tag, activation function como softmax (soma tudo ate 1, mostrando a probabilidade)
            Dense(len(output[0]), activation="softmax")
        ]
    )   

#Gradient descent (with momentum) optimizer. Parte q eu n entendo, mas a internet é boa, eu confio.
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) 

"""
loss funciton como categorical_crossentropy
optimizer como o que acabamos de declrar em cima
e o objeto é acerto (metrics)
"""
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"]) #configurar o modelo

"""
np.array(inputs) como input 
np.array(output) como output
trinar 200 vezes
batch_size=5, ou seja, a cada 5 iterações ele atualizará os pesos
"""

trained_model = model.fit(np.array(inputs), np.array(output), epochs=200, batch_size=5) #treinar o modelo