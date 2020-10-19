import sys; args = sys.argv[1:]
# Krish Ganotra - Backprop 1
import re
import math
import random
import time

global transType
transfers = {'T1':lambda x: x, 'T2': lambda x: max(0,x), 'T3': lambda x: 1/(1+math.exp(-x)), 'T4': lambda x: (-1 + 2/(1+math.exp(-x)))}
transDerivs = {'T1': lambda y:1, 'T2': lambda y: 1 if y>1 else 0, 'T3': lambda y: y*(1-y), 'T4': lambda y: (1-y*y)/2}
transType = 'T3'

def dot(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])

def feedforward(inputs, weights):
    global transType
    ffInfo = [inputs]
    currLayer = inputs
    lastLayer = weights[-1]
    for k in range(len(weights)-1):
        layerWeights = weights[k]
        layerOutputs = []
        for j in range(0,len(layerWeights),len(currLayer)):
            layerOutputs.append(transfers[transType](dot(currLayer,layerWeights[j:j+len(currLayer)])))
        ffInfo.append(layerOutputs)
        currLayer = layerOutputs
    finalOutput = [currLayer[i]*lastLayer[i] for i in range(len(currLayer))]
    ffInfo.append(finalOutput)
    return ffInfo

def backProp(weights, ffInfo, output):
    backInfo = [layer.copy() for layer in ffInfo]

    for i in range(len(backInfo[-1])): #last layer *special case*
        backInfo[-1][i] = output[i] - ffInfo[-1][i]
    for i in range(len(backInfo[-2])): #second to last layer *special case*
        backInfo[-2][i] = backInfo[-1][i] * weights[-1][i] * transDerivs[transType](ffInfo[-2][i])
    for k in range(len(backInfo)-3,0,-1):
        for i in range(len(backInfo[k])):
            total = sum([weights[k][i*len(backInfo[k+1])+j] * backInfo[k+1][j] for j in range(len(backInfo[k+1]))])
            backInfo[k][i] = total*transDerivs[transType](ffInfo[k][i])
    return backInfo

def gradientDescent(weights, backInfo, ffInfo, alpha):
    for k in range(len(weights)):
        for i in range(len(weights[k])//len(backInfo[k+1])):
            for j in range(len(backInfo[k+1])):
                weights[k][i+j*len(backInfo[k])] += backInfo[k+1][j] * ffInfo[k][i] * alpha
    return weights

def errorAll(weights, testCases):
    all = []
    for test in testCases:
        output = feedforward(test[0],weights)[-1]
        expected = test[1]
        all.append(1/2 * sum([(output[i]-expected[i])**2 for i in range(len(output))]))
    return all


file = open(args[0])
layerLens = []
testCases = [] #list of tuples (each tuple is (input, output) where both input and output are repersented in lists)
for line in file:
    data = line.strip().split(' ')
    ind = data.index('=>')
    if(not layerLens): layerLens = [ind+1, 2, 1,len(data)-ind-1]
    testCases.append(([int(x) for x in data[:ind]]+[1], [int(x) for x in data[ind+1:]]))


weights = [[0]*(layerLens[k]*layerLens[k+1]) for k in range(len(layerLens)-1)]

finished = False

while (True):
    #print('STARTINGGGGGGGGG')
    alpha = .3

    #start = time.time()
    ago10 = 100
    modulo = 0
    if(finished): break
    for k in range(len(weights)):
        for i in range(len(weights[k])):
            weights[k][i] = random.uniform(-2,2)
    E = errorAll(weights, testCases)
    bestE = sum(E)
    if(bestE > 5):
        continue
    # print('error', bestE)
    # print('Layer cts:', layerLens)
    # print('Weights:')
    # for x in weights: print(x)

    lastTime = 0
    while True:
        # if(time.time()-start > 6 and bestE > 0.1):
        #     alpha += 0.01
        #     break
        if(sum(E) > 0.1 and modulo%10 == 0):
            if(ago10 - bestE < 0.0001):
                break
            ago10 = bestE
        modulo += 1

        for testCase in range(len(testCases)):
            lastTime += 1
            ffInfo = feedforward(testCases[testCase][0],weights)
            backInfo = backProp(weights, ffInfo, testCases[testCase][1])
            weights = gradientDescent(weights, backInfo, ffInfo, alpha)

            output = ffInfo[-1]
            expected = testCases[testCase][1]
            E[testCase] = 1/2 * sum([(output[i]-expected[i])**2 for i in range(len(output))])
        #print('new weights', weights)

        if(sum(E)<bestE):
            bestE = sum(E)
            if(lastTime > 100000):
                print()
                print('error', bestE)
                print('Layer cts:', layerLens)
                print('Weights:')
                for x in weights: print(x)

                lastTime = 0
            #print('Error at iteration {0}: {1}'.format(i,bestE))
        #print('New error', E)
        if(bestE < 0.01):
            # print('we did it boys')
            # print('one small step for man, one giant leap for mankind')
            # print('yeeted')
            # print('Ha gottem')
            # print('gg')
            # print('Got the horses in the back propogation')
            # print('')
            yeeted = True
            finished = True
            break

print('FINAL ERROR', bestE)
print('Layer cts:', layerLens)
print('Weights:')
for x in weights: print(x)

#every 10 times when error is above 0.1
# if error from 10 times ago minus error now is <0.0001 then restart

'''
set random weights  <>
forward propogate   <>
backward propogate  <>
calc gradients      <>
adjust weights      <>
print out new error
repeat


data structures
    - weights (# of nodes in layer k * # of nodes in layer k+1 size)
    - feedforward results (# of nodes per layer size)
    - errors (ff results size)
    - gradients (weights size)
'''
