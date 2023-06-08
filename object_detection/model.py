import torch.nn as nn
import torch

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
    #o 4 signfica que os filtros vão ser repetidos 4 vezes
    [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
    (3, 1024, 1, 1),
    (3, 1024, 2, 1), 
    (3, 1024, 1, 1),
    (3, 1024, 1, 1),
]

class CNNBlock(nn.Modu):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        self.conv = nn.Convd2d(in_channels, out_channels, bias=False, **kwargs)                
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)

    def foward(self, x):
        return self.leakyrelu(self.batchnorm(self.conv(x)))
    
class Yolov1(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        def __init__(self, in_channels=3, **kwargs):
            super(Yolov1, self).__init__()
            self.architecture = architecture_config
            self.in_channels = in_channels,
            self.darknet = self.create_conv_layers(self.architecture)
            self.fcs = self.create_fcs(**kwargs)

        def foward(self, x):
            x = self.darknet(x)
            return self.fcs(torch.flatten(x, start_dim=1))

        def _create_conv_layers(self, architecture):
            layers = []
            in_channels = self.in_channels

            for x in architecture:
                if type(x) == tuple:
                    layers += [
                        CNNBlock(
                        in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3]
                        )   
                    ]
                elif type(x) == str:
                    layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
                
                elif type(x) == list:
                    conv1 = x[0] #filtro 1
                    conv2 = x[1] #filtro 2
                    num_repeats = x[2] #quantas vezes esses filtros vão se repetir

                    for _ in range(num_repeats):
                        layers += [
                            CNNBlock(
                                in_channels,
                                conv1[1],
                                kernel_size=conv1[0],
                                stride=conv1[2],
                                padding=conv1[3]
                            )
                        ]

                        layers += [
                            CNNBlock(
                                conv1[1], #in_channel vai ser o otuput da priemira layer convolucional
                                conv2[1], 
                                kernel_size=conv2[3],
                                padding=conv2[3]

                            )
                        ]

                        in_channels = conv2[1]
                        
            return nn.Sequential(*layers)