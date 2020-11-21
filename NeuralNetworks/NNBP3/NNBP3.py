import sys; args=sys.argv[1:]
#Krish Ganotra -- BackProp3
import re
import math
import random
import time

def insert(list, element, startIndex, stepIndex):
    i = startIndex
    temp = [x for x in list]
    while(i<len(temp)):
        temp.insert(i, element)
        i += stepIndex
    return temp

equation = args[1]
regex = re.search(r'(>|<)=?([.0-9]+)', equation)

r2 = 1
greater = True
greater, r2 = regex.groups()
greater = greater=='>'
r2 = float(r2)
r = r2**(1/2)
print("Equation:", args[1])


global transType
transfers = {'T1':lambda x: x, 'T2': lambda x: max(0,x), 'T3': lambda x: 1/(1+math.exp(-x)), 'T4': lambda x: (-1 + 2/(1+math.exp(-x)))}
transDerivs = {'T1': lambda y:1, 'T2': lambda y: 1 if y>1 else 0, 'T3': lambda y: y*(1-y), 'T4': lambda y: (1-y*y)/2}
transType = 'T3'

squarerFile = open(args[0])
SquarerWeights = []

print("Squarer File:")
for line in squarerFile:
    line = line.strip()
    print(line)
    layer = [float(w) for w in re.findall(r'-?\d*[.]?\d*', line) if(w)]
    if(layer): SquarerWeights.append(layer)

print()
SquarerLayerLens = [2]
for i in range(len(SquarerWeights)):
    SquarerLayerLens.append(len(SquarerWeights[i])//SquarerLayerLens[i])

print('SquarerLayerLens:', SquarerLayerLens)
print('Squarer Weights')
for x in SquarerWeights: print(x)
print()

weights = []
layerLens = [3] + [x*2 for x in SquarerLayerLens[1:-2]] + [2, 1, 1]

SquarerWeights[0] = [x if i%2 else x/r for i,x in enumerate(SquarerWeights[0])]
weights.append(insert(SquarerWeights[0],0,1,3) + insert(SquarerWeights[0],0,0,3))

for i in range(1, len(SquarerWeights)-1):
    SquarerLayer = SquarerWeights[i]
    layerCt = SquarerLayerLens[i]

    empty = [0]*layerCt

    layer = []
    for j in range(SquarerLayerLens[i+1]):
        layer += SquarerLayer[j*layerCt:(j+1)*layerCt] + empty
    for j in range(SquarerLayerLens[i+1]):
        layer += empty + SquarerLayer[j*layerCt:(j+1)*layerCt]
    weights.append(layer)

weights.append(SquarerWeights[-1]*2)

if(greater):
    weights.append([(1+math.e)/(2*math.e)])
else:
    weights[-1] = [-x for x in weights[-1]]
    weights.append([(1+math.e)/2])

print('Layer cts:', layerLens)
print('Weights:')
for layer in weights: print(layer)
