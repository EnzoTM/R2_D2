import json
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer #reduz palavras diferentes para uma só

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers.legacy import SGD
from keras.models import load_model
import sys

import string

class language:
    def __init__(self, arquivo, file_words, file_classes, file_model, training=False):
        #trinamento
        self.training = training
        
        #arquaivo json a ser lido
        self.arquivo = arquivo

        #arquivo

        #variavel que armazenará o nome do arquivo de words, classes e model
        self.file_words = file_words
        self.file_classes = file_classes
        self.file_model = file_model

        #declarar as listas para o trainamento
        self.words = []
        self.classes = []
        self.instancias = []

        #declarar as listas para o predict
        self.words_P = []
        self.classes_P = []

        #carregar o modelo se n estiver sendo treinado
        if not self.training:
            self.model = load_model(self.file_model)  

        #ler o arquivo json programa/padroes.json
        self.padroes = json.loads(open(self.arquivo).read())

        self.lemmatizer = WordNetLemmatizer()
    
    def load(self):
        """
        carregar o arquaivo json para as listas
        """
        #carregar do arquivo json para as listas
        for padrao in self.padroes["padroes"]:
            #para cada padrao dentro do nosso arquivo json
            for input_ in padrao["input"]:
                #dividir a frase palavra por palavra
                word_list = nltk.word_tokenize(input_) 

                #adicionar as palavras na lista words
                for word in word_list:
                    self.words.append(word)

                print(padrao["index"])

                #adicionar a lista de palavras + a classe na lista de instanciaos
                self.instancias.append((word_list, padrao["classe"]))

                #se esta categoria ainda nao foi adicionada em calsses, adiciona-la
                if padrao["classe"] not in self.classes:
                    self.classes.append(padrao["classe"])

        '''
        #lemmatizar as palavras
        for i in range(0, len(word_list)):
            word_list[i] = self.lemmatizer.lemmatize(word_list[i])'''
        
        #ver todas as palavras que teremos de remover, e remove-las
        words_to_remove = []

        for word in self.words:
            if word in string.punctuation:
                words_to_remove.append(word)

        for word in words_to_remove:
            self.words.remove(word)

        #colocar words como set, pois assim nenhuma palavra ira se repetir
        self.words = list(set(self.words))

        #organizar as palavras
        self.words = sorted(self.words)

        #organizar as classes
        self.classes = sorted(self.classes)

        #salvar as palavras em um arquivo
        with open(self.file_words, "w") as f:
            for word in self.words:
                f.write(word + " ")

        #salvar as classes em um arquivo
        with open(self.file_classes, "w") as f:
            for classe in self.classes:
                f.write(classe + " ")
    
    #sessão de treinamento da ia

    def load_training(self):
        """
        transformar os inputs e os outputs para binário
        retorna duas listas, em np.array, uma do input e outra do output
        """
        binary_input = [] #lista que irá conter todos os inputs em binário
        binary_output = [] #lista que irá conter todos os outputs em binário

        #para cad instancia (classe com suas palavras)
        for instancia in self.instancias:
            b_output = [0] * len(self.classes) #criar o array de binário do output
            b_input = [] #criar o array em binário do input

            #pegar as palavras da classe
            word_from_class = instancia[0]

            #para cada palavra de todas as palavras
            for word in self.words:
                if word in word_from_class:
                    b_input.append(1) #se esta palavra estiver presente nas palavras da classe
                else:
                    b_input.append(0) #se esta palavra nao estiver presente nas palavras da classe
            
            #adicionar o array das palavras para a lista
            binary_input.append(b_input)

            #b_output é uma lista com o tamanho sendo o número de classes. Logo, no index desta classe vamos seta-la como 1 para sabermos de qual classe estamos falando
            b_output[self.classes.index(instancia[1])] = 1

            #adicionar o b_output na lista de outputs
            binary_output.append(b_output)

        #retornar eles como np.array
        return np.array(binary_input), np.array(binary_output)
    

    def create_model(self, inputs, outputs):
        #cirar o medelo 

        print(f"Input ta assim: {len(inputs[0])}")

        model = Sequential(
            [
                #128 input layers, com o tamanho do numero de palavras, e o a activation funcion como relu
                Dense(128, activation="relu", input_shape=(len(inputs[0]),)), 
                #50% de dropout
                Dropout(0.5),
                #64 hidden layers, com acitivation function como relu
                Dense(64, activation="relu"),
                #50% de dropout
                Dropout(0.5),
                #x outptus layers, onde x = numero de classe, activation function como softmax (soma tudo ate 1, mostrando a probabilidade)
                Dense(len(outputs[0]), activation="softmax")
            ]
        )   

        #Gradient descent (with momentum) optimizer. Parte q eu n entendo, mas a internet é boa, eu confio.
        sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

        """
        loss funciton como categorical_crossentropy
        optimizer como o que acabamos de declrar em cima
        e o objeto é acerto (metrics)
        """
        model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"]) #configurar o modelo

        """
        np.array(inputs) como input 
        np.array(outputs) como output
        trinar 200 vezes
        batch_size=5, ou seja, a cada 5 iterations ele atualizará os pesos
        """
        
        trained_model = model.fit(np.array(inputs), np.array(outputs), epochs=200, batch_size=5) #treinar o modelo

        model.save("arquivos/models/model.model", trained_model)

        return model, trained_model

    """
    #criar o modelo, e amrazena-lo em model e trained_model
    model, trained_model = self.create_model(inputs, outputs)

    #salvar o modelo em model.model
    model.save("model.model", trained_model)
    """
    
    #sessão de predição da ia
    def load_files(self):
        """
        carrega os arquivos (words, classes e modelo)
        """

        #ler dos arquivos para as listas
        with open(self.file_words, "r") as f:
            words = f.read()

            self.words_P = words.split()    
        
        with open(self.file_classes, "r") as f:
            classes = f.read()

            self.classes_P = classes.split()     
        
        self.model = load_model(self.file_model)  


    def filter_sentence(self, sentence):
        """
        filtrar a sentença
        """
        #tekenzalizar a frase
        sentence_words = nltk.word_tokenize(sentence)

        #filtrar as palavras na frase
        words_to_remove = []

        for word in sentence_words:
            if word in string.punctuation:
                words_to_remove.append(word)
        
        for word in words_to_remove:
            sentence_words.remove(word)

        return sentence_words
    

    def sentece_to_words(self, sentence):
        """
        pegar a frase, e passa-la para palavras
        """
        #pegar as palavras da frase
        words_from_the_sentece = self.filter_sentence(sentence)

        #criar a lista com o tamanho do numero de palavras, onde cada parte é 0 para podermos identificar qual palavra é qual
        binary_words = [0] * len(self.words_P)

        #para cada palavra da frase
        for w in words_from_the_sentece:
            #para cada palavra em words
            for i, word in enumerate(self.words_P):
                #se as palavras forem a mesma, colocar 1 nesse index
                if word == w:
                    binary_words[i] = 1

        print(binary_words)

        return np.array(binary_words) 
    

    def get_classe(self, sentece):
        """
        predizir a classe
        """
        words_from_the_sentece = self.sentece_to_words(sentece) 
        #predicar o resultado baseado nas palavras

        print(f"classe: {len(self.classes_P)}")

        result = self.model.predict(np.array([words_from_the_sentece]))[0]

        print(result)

        margem_de_erro = 0.25 

        #i = index, r = resultado. Se o resultado for maior do que a margem de erro, iremos enumera-lo
        result = [[i, r] for i, r in enumerate(result) if r > margem_de_erro]

        #ordernar por probabilidade, da maior para a menor
        result.sort(key=lambda x: x[1], reverse=True) 

        

        #return {"classe": self.classes_P[result[0][0]], "probabilidade": str(result[0][1])}
        return self.classes_P[result[0][0]]