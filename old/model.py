import torch.nn as nn
import torch

#architecture model provided by: https://arxiv.org/pdf/1506.02640v5.pdf
#model implementation code provided by: Aladdin Persson

"""
cada tupla será organizada da seguinte maneira:
t[0] = kernel size (nxn)
t[1] = número de filtros
t[2] = stride
t[3] = padding

O M se refere ao max-pooling com slider de 2

Toda a arquitetrua está explicada no documento
"""
architecture_config = [
    (7, 64, 2, 3),
    "M",
    (3, 192, 1, 1),
    "M",
    (1, 128, 1, 0),
    (3, 256, 1, 1),
    (1, 256, 1, 0),
    (3, 512, 1, 1),
    "M",
    #o 4 signfica que os filtros vão ser repetidos 4 vezes
    [(1, 256, 1, 0), (3, 512, 1, 1), 4],
    (1, 512, 1, 0),
    (3, 1024, 1, 1),
    "M",
    #o 2 signfica que os filtros vão ser repetidos 2 vezes
    [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
    (3, 1024, 1, 1),
    (3, 1024, 2, 1), 
    (3, 1024, 1, 1),
    (3, 1024, 1, 1),
]

class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        #a Convolutional Layer vai ter como input o número de canais de entrada, os canais de saida + os argumentos sobre kernel, slider e padding (**kwargs)
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)                
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)

    def forward(self, x):
        return self.leakyrelu(self.batchnorm(self.conv(x)))
    
class Yolov1(nn.Module):
    def __init__(self, in_channels=3, **kwargs): 
        ''' Informações a serem passadas no **kwargs
        split_size --> recomendado como 7, entretanto, pode-se aumentar o número para maior detecção de objetos
        num_box --> sendo 2, 1 box de altura e outra box de largura
        num_classes --> 20, pois são as 20 classes padrões do yolo
        '''
        super(Yolov1, self).__init__()
        self.architecture = architecture_config #a arquitetura do modelo vai ser baseada na arquitetura do artigo: https://arxiv.org/pdf/1506.02640v5.pdf (descrita na lista architecture_config)
        self.in_channels = in_channels #inicialmente o input será de 3 (as 3 camadas RGB)
        self.darknet = self.create_conv_layers(self.architecture) #criação das layers, nas quais foram chamadas de darknet no artigo
        self.fcs = self.create_fcs(**kwargs) #dar um flatten na imagem + activation_function e outros parametros para que as informações fiquem bonitinhas no output

    def forward(self, x):
        x = self.darknet(x)
        return self.fcs(torch.flatten(x, start_dim=1))

    def create_conv_layers(self, architecture):
        layers = []
        in_channels = self.in_channels #o input inicial vai ser de 3 (rgb)
        
        #adicionar as layers no modelo
        #na lista da arquitetrua, separamos em 3 cateogrias, tupla (1 CL), string (Max-Pooling), list (Mais de uma CL com repetição)
        for x in architecture:
            if type(x) == tuple:
                layers += [
                    CNNBlock(
                    in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3], #criar a nova Cl com suas especificidades
                    )   
                ]

                in_channels = x[1] #o novo in_channel tem que ser alterado, pois quando se apalica o filtro, o pŕoximo input vai ter a mesma quantidade de camadas do filtro aplicado

            elif type(x) == str:
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)] #colocar a camada de Max-Pooling
            
            elif type(x) == list:
                conv1 = x[0] #filtro 1
                conv2 = x[1] #filtro 2
                num_repeats = x[2] #quantas vezes esses filtros vão se repetir

                for _ in range(num_repeats): #criar a msm CV repetida por num_repeats
                    layers += [
                        CNNBlock(
                            in_channels,
                            conv1[1],
                            kernel_size=conv1[0],
                            stride=conv1[2],
                            padding=conv1[3],
                        )
                    ]

                    layers += [
                        CNNBlock(
                            conv1[1], #in_channel vai ser o otuput da priemira layer convolucional
                            conv2[1], 
                            kernel_size=conv2[0],
                            stride=conv2[2],
                            padding=conv2[3],

                        )
                    ]

                    in_channels = conv2[1] #o novo in_channel tem que ser alterado, pois quando se apalica o filtro, o pŕoximo input vai ter a mesma quantidade de camadas do filtro aplicado
                    
        return nn.Sequential(*layers)
    
    def create_fcs(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes

        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 496), # no artigo deveria ser 4096, mas para n consumir muita ram diminui-se para 496
            nn.Dropout(0.0),
            nn.LeakyReLU(0.1),
            nn.Linear(496, S * S * (C + B * 5)) # o final deve ser (S, S, 30), logo C + B * 5 = 30
        )

def test(S=7, B=2, C=20):
    model = Yolov1(split_size=S, num_boxes=B, num_classes=C)
    x = torch.randn((2, 3, 448, 448)) 
    print(model(x).shape)

test()