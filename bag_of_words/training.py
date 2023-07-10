import json
import pickle
import numpy as np

import random


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

#guardar as calsses e palavras em um arquivo
pickle.dump(palavras, open("palavras.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

training = []
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

    training.append([bag, output])

random.shuffle(training)
training = np.array(training)

training_x = []

training_y = []

for i in range(0, len(training[0])):
    training_x.append(training[0][i])

for i in range(0, len(training[1])):
    training_y.append(training[1][i])

model = Sequential()
model.add(Dense(128, input_shape=(len(training_x[0],), activation="relu"))) 
model.add(Dropout(0.5))
model.add(Desne(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Desne(len(training_y[0]), activation="softmax"))

sgd = SGD(Ir=0.01, decay=1e-6, momentum=0.9, nestrov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

model.fit(np.array(training_x), np.array(training_y), epochs=200, batch_size=5, verbose=1)

model.save()