import sys; args = sys.argv[1:]
#Krish Ganotra - Feed Forward
import math

weights = open(sys.argv[1])
transferType = sys.argv[2]
inputs = [float(x) for x in sys.argv[3:]]

def makeTransferFunc(tType = 'T1'):
    if(tType == 'T1'):
        return lambda x: x
    elif(tType == 'T2'):
        return lambda x: max(0,x)
    elif(tType == 'T3'):
        return lambda x: 1/(1+math.exp(-x))
    elif(tType == 'T4'):
        return lambda x: (-1 + 2/(1+math.exp(-x)))

def dot(a,b):
    return sum(a[i]*b[i] for i in range(len(a)))

transfer = makeTransferFunc(transferType)

layerWeights = []
for layer in weights:
    layerWeights.append([float(x) for x in layer.strip().split(' ')])

finalLayer = layerWeights.pop()

ffInfo = [inputs]
currLayer = inputs

# print("Layer Weights:", layerWeights)
# print("Final Layer:", finalLayer)
# print("ffInfo:", ffInfo)
# print("currLayer:", currLayer)
# print()

for k in range(len(layerWeights)):
    currLayerWeights = layerWeights[k]
    layerOutputs = []
    for j in range(0,len(currLayerWeights),len(currLayer)):
        layerOutputs.append(transfer(dot(currLayer,currLayerWeights[j:j+len(currLayer)])))
    ffInfo.append(layerOutputs)
    currLayer = layerOutputs

inputs = ffInfo[-1]

inputs = [inputs[i]*finalLayer[i] for i in range(len(inputs))]
ffInfo.append(inputs)

# print('Feedforward Info (node values):', ffInfo)
# print('Output:', ' '.join(map(str,inputs)))
print(' '.join(map(str,inputs)))
