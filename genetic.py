import numpy as np
import random
import neural_network as nn

def crossover(net1 = nn.NeuralNetwork(), net2 = nn.NeuralNetwork(), rate = 0.0):
    # First check if the neutral network are of the same length before crossing over
    isValid = True
    if len(net1.input) != len(net2.input):
        isValid = False
    for i in range(len(net1.hidden)):
        if len(net1.hidden[i]) != len(net2.hidden[i]):
            isValid = False
    if len(net1.output) != len(net2.output):
        isValid = False
    hidden_length = 0
    if len(net1.hidden) > 0:
        hidden_length = len(net1.hidden[0])
    if isValid:
        new_net = nn.NeuralNetwork(len(net1.input), hidden_length, len(net1.hidden), len(net1.output))
        for l in range(len(net1.hidden)):
            cross = rate * net1.hidden[l].size()
            cross_list = list()
            for c in range(cross):
                isValid = False
                x,y = (0,0)
                while not isValid:
                    y = random.randint(net1.hidden[l].shape()[0])
                    x = random.randint(net1.hidden[l].shape()[1])
                    if (x,y) not in cross_list:
                        isValid = True
                cross_list.append((x,y))
            for c in cross_list:
                new_net.hidden[l][c[1]][c[0]] = net2.hidden[l][c[1]][c[0]]
        return new_net
    else:
        print("Not Valid")
                
def mutation(net = nn.NeuralNetwork(), mutation = 0):
    # Change weights by random
    mutated_weight = []
    for mut in mutation:
        isValid = False
        while not isValid:
            l = random.randint(net.hidden.shape()[0])
            x = random.randint(net.hidden.shape()[1])
            y = random.randint(net.hidden.shape()[2])
            if (l,x,y) not in mutated_weight:
                net.hidden[l][y][x] = random.random()
                mutated_weight.append((l,x,y))


