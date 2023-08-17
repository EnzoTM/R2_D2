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
            #declaração das listas que serão necessárias para a predição
            self.palavras_predicao = []
            self.classes_predicao = []
        
        #declaração de variáveis que serão necessárias em ambas as ocasiões
        self.arquivo_palavra = arquivo_palavra
        self.arquivo_classe = arquivo_classe
        self.arquivo_modelo = arquivo_modelo

    def load_json_to_list(self):
        """
        *carrega as palavras e classes do arquivo json para as listas
        *salva as palavras filtradas e as classes em um arquivo txt
        """
        #para cada instancia
        for instancia in self.arquivo_instancias["instancia"]:
            #para cada frase nas listas de frases da instancia
            for frase in instancia["frases"]:
                #transformando a frase em uma lista de palavras
                lista_palavras = nltk.word_tokenize(frase)

                #adicionar cada palavra nas listas de palavras
                for palavra in lista_palavras:
                    self.palavras.append(palavra)

            #adicionar 
            self.classes.append(instancia["classe"])

    def treinamento(self):
        #verificar se a variável treinamento foi devidamente inicializada
        if not(self.treinamento): 
            raise Exception("Treinamento nao inicializado!")

        self.load_json_to_list()


