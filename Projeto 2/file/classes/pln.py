import json
import numpy as np
import os

import nltk

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers.legacy import SGD
from keras.models import load_model
import sys

import string

class language():
    def __init__(self, arquivo_palavra, arquivo_classe, arquivo_modelo, arquivo_instancias=None, treinamento=False):
        if treinamento:
            #declaração das listas que serão necessárias para o treinamento
            self.palavras = []
            self.classes = []
            self.instancias = []
            
            #verificar se o arquivo json foi passado como argumento
            if arquivo_instancias == None:
                raise Exception("Arquivo com padrões não fornecido!")

            #ler o arquivo json
            self.arquivo_instancias = json.loads(open(arquivo_instancias).read())
        else: 
            #ler os arquivos jsons referentes as palavras e as classes
            self.palavras_predicao = json.loads(open(self.arquivo_palavra).read())
            self.classes_predicao = json.loads(open(self.arquivo_classe).read())

            #carregar o modelo
            self.modelo = load_model(self.arquivo_modelo)
        
        #declaração de variáveis que serão necessárias em ambas as ocasiões
        self.arquivo_palavra = arquivo_palavra
        self.arquivo_classe = arquivo_classe
        self.arquivo_modelo = arquivo_modelo

    def carregar_json_para_lista(self):
        """
        *carrega as palavras e classes do arquivo json para as listas
        *salva as palavras filtradas e as classes em um arquivo txt
        """
        #para cada instancia
        for instancia in self.arquivo_instancias["instancia"]:
            #lista que irá conter as palavras das frases
            lista_palavras_local = []

            #para cada frase nas listas de frases da instancia
            for frase in instancia["frases"]:
                #transformando a frase em uma lista de palavras
                palavras_da_frase = nltk.word_tokenize(frase)

                #adicionar cada palavra nas listas de palavras global
                for palavra in palavras_da_frase:
                    self.palavras.append(palavra)

                    #adicionar a palavra se ela não estiver na lista de palavras local
                    if palavra not in lista_palavras_local:
                        lista_palavras_local.append(palavra)

            #adicionar a classe na lista de classes
            self.classes.append(instancia["classe"])

            #adicionar a nova instancia a lista de instancias
            self.instancias.append((lista_palavras_local, instancia["classe"]))
        
        #listas das palavras que devem ser removidas
        palavras_para_remocao = []

        #para cada palavra
        for palavra in self.palavras:
            #remover as pontuações
            if palavra in string.punctuation: 
                palavras_para_remocao.append(palavra)
        
        #remover todas as palavras presentes na lista de palavras para remoção
        for palavra in palavras_para_remocao:
            self.palavras.remove(palavra)

        #remover todas as palavras duplicadas
        self.palvras = list(set(self.palavras))

        #armazenar as palavras no arquivo json de palavras
        with open(self.arquivo_palavra, "w") as f:
            json.dump(self.palavras, f)

        #armazenar as classes no arquivo json de classes
        with open(self.arquivo_classe, "w") as f:
            json.dump(self.classes, f)

    def inputs_outputs_to_binary(self):
        """
        *pega os inputs e os transforma em binário para que possam ser alimentados no modelo
        *retorna as listas dos inputs e outputs de cada instancia em binário no formato de um numpy array
        """
        #listas de como vai ficar os inputs e outputs em binário
        binary_inputs = []
        binary_outputs = []

        #para cada instancia
        for instancia in self.instancias:
            instancia_binary_output = []
            instancia_binary_input = []

            #pegar as palavras referente a esta instancia
            palavras_da_instancia = instancia[0]

            #para cada palavra ja registrada
            for palavra in self.palavras:
                #se a palavra fizer parte da lista de palavras da instancia atual
                if palavra in palavras_da_instancia:
                    instancia_binary_input.append(1) #adicionar 1 na lista
                else: 
                    instancia_binary_input.append(0) #adicionar 0 na lista
            
            #adicionar a lista das palavras em binário da instancia atual na lista de todas as instancias
            binary_inputs.append(instancia_binary_input)

            #para cada classe ja registrada
            for classe in self.classes:
                #se for a mesma classe da instancia atual
                if classe == instancia["classe"]:
                    instancia_binary_output.append(1) #adicionar 1 na lista
                else:
                    instancia_binary_output.append(0) #adicionar 0 na lista
            
            #adicionar a lista de classes em binário da instancia atual na lista de todas as instancias
            binary_outputs.append(instancia_binary_output)
        
        #retornar as listas em forma de np.array (necessário para que possa ser alimentado no modelo)
        return np.array(binary_inputs), np.array(binary_outputs)

    def treinar_modelo(self, inputs, outputs):
        #cirar o medelo 

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
        
        #salvar o modelo
        model.save(self.arquivo_modelo, trained_model)

    def treinamento(self):
        #verificar se a variável treinamento foi devidamente inicializada
        if not(self.treinamento): 
            raise Exception("Treinamento nao inicializado!")

        self.carregar_json_para_lista()

        inputs_binary, outputs_binary = self.inputs_outputs_to_binary()

        self.treinar_modelo(inputs_binary, outputs_binary)

        print("Treinamento feito!")

    def filtrar_frase(self, frase):
        """
        *filtrar a frase
        *retornar uma lista com as palavras filtradas
        """
        palavras = nltk.word_tokenize(frase)

        #filtrar as palavras na frase
        palavras_para_remover = []

        for word in palavras:
            if word in string.punctuation:
                palavras_para_remover.append(word)
        
        for word in palavras_para_remover:
            palavras.remove(word)

        return palavras

    def preidcao(self, frase):
        """prediz a classe dado uma frase"""
        palavras_filtradas = self.filtrar_frase(frase)

        #lista que irá conter  nossas palavras em binário
        palavras_binario = []

        for palavra in self.palavras:
            if palavra in palavras_filtradas:
                palavras_binario.append(1)
            else:
                palavras_binario.append(0)

        #transformar a nossa lista em um numpy array para alimentar o modelo
        palavras_binario = np.array(palavras_binario)

        resultado = self.modelo.predict(palavras_binario)[0]

        #ordernar por probabilidade, da maior para a menor
        resultado.sort(key=lambda x: x[1], reverse=True) 

        #return {"classe": self.classes_P[result[0][0]], "probabilidade": str(result[0][1])}
        return self.classes_P[resultado[0][0]]
