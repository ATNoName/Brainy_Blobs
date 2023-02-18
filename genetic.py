import random
import neural_network as nn
import player
import copy

def crossover(net1: nn.NeuralNetwork, net2: nn.NeuralNetwork, rate = 0.0):
    # First check if the neutral network are of the same length before crossing over
    isValid = True
    if net1.input_length != net2.input_length:
        isValid = False
    for i in range(len(net1.hidden)):
        if len(net1.hidden[i]) != len(net2.hidden[i]):
            isValid = False
    if net1.output_length != net2.output_length:
        isValid = False
    hidden_length = 0
    if len(net1.hidden) > 1:
        hidden_length = len(net1.hidden[0])
    if isValid:
        new_net = copy.deepcopy(net1)
        for l in range(len(net2.hidden)):
            cross = round((1 - rate) * len(net2.hidden[l]))
            cross_list = list()
            for c in range(cross):
                isValid = False
                x,y = (0,0)
                while not isValid:
                    y = random.randint(0, len(net2.hidden[l][0])-1)
                    x = random.randint(0, len(net2.hidden[l])-1)
                    if (x,y) not in cross_list:
                        isValid = True
                cross_list.append((x,y))
            for c in cross_list:
                new_net.hidden[l][c[0]][c[1]] = net2.hidden[l][c[0]][c[1]]
        return new_net
    else:
        print("Not Valid")
                
def mutate(net: nn.NeuralNetwork, mutation = 0):
    # Change weights by random
    mutated_weight = []
    for mut in range(mutation):
        isValid = False
        while not isValid:
            l = random.randint(0,len(net.hidden)-1)
            x = random.randint(0,len(net.hidden[l])-1)
            y = random.randint(0,len(net.hidden[l][0])-1)
            if (l,x,y) not in mutated_weight:
                net.hidden[l][x][y] = random.random()
                mutated_weight.append((l,x,y))
                isValid = True
    return net

def fitness(atkplayer: player.Player, player_list: list[player.Player]):
    # return a neural network
    randplayer = random.choice(player_list)
    atkbignet = atkplayer.bignet
    atksmallnet = atkplayer.smallnet
    randbignet = randplayer.bignet
    randsmallnet = randplayer.smallnet
    newbignet = mutate(crossover(atkbignet,randbignet, 0.7), 5)
    newsmallnet = mutate(crossover(atksmallnet,randsmallnet, 0.7), 5)
    return newbignet, newsmallnet
