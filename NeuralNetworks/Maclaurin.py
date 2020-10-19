'''
maclaurin series for T3: 1/2 + 1/4x - 1/48 x^3 + 1/480 x^5 - 17/80640 x^7
polynomial structure: list of terms
term structure: [coefficient, x power, y power]

'''
import sys


layerCts = [3, 4, 3, 1, 1]
weights = [[4.5612, 0.3306, 2.2676, -2.722, 3.7759, 2.1807, 1.7313, 4.1411, -2.3184, 0.028, -0.2594, 2.1547], [-0.5744, -3.7962, 3.5616, 0.4858, -6.1672, -5.5007, 6.5999, 6.7361, 2.4203, 1.9587, -0.1342, -1.2748], [-4.4649, -11.7595, 6.063], [1.0677]]
cutOff = 0.1 #threshold for printing, higher value -> more aesthetic; lower value -> more info
inputLayer = [[[1,1,0]],[[1,0,1]],[[1,0,0]]] #[x, y, 1]

def polyMult(poly1, poly2): #multiplies two polynomials together
    newPolyDict = {} #easier to search for like terms in a dictionary
    for term1 in poly1:
        for term2 in poly2:
            newCoeff, newXPow, newYPow = term1[0]*term2[0], term1[1]+term2[1], term1[2]+term2[2]
            key = (newXPow, newYPow)
            if(key in newPolyDict):
                newPolyDict[key] += newCoeff
            else:
                newPolyDict[key] = newCoeff

    return [[newPolyDict[powers], powers[0], powers[1]] for powers in newPolyDict] #put dictionary back into polynomial form

def polyPow(poly, pow, const=1): #raises poly to the 'pow'th power and then multiplies by the const
    if(pow==0):
        return [[1*const, 0, 0]]

    toBeMult = [poly for i in range(pow)]
    while(len(toBeMult)>1):
        toBeMult.append(polyMult(toBeMult.pop(), toBeMult.pop()))

    outputPoly = toBeMult[0]
    for term in outputPoly: term[0] *= const
    return outputPoly

def polyprint(poly): #prints out polynomials aesthetically
    string = ''
    for i,term in enumerate(poly):
        coeff, xPow, yPow = term
        if abs(coeff) > cutOff:
            if i != 0:
                sign = '+ ' if coeff > 0 else '- '
                string += sign
            if not (abs(coeff) == 1 and term[1] + term[2] > 0):
                string += "{:.2f}".format(abs(coeff))
            if xPow != 0:
                if xPow == 1:
                    string += 'x'
                else:
                    string += 'x^'+str(term[1])
            if yPow != 0:
                if yPow == 1:
                    string += 'y'
                else:
                    string += 'y^'+str(term[2])
            string += ' '
    print(string)

def polycomb(poly): #combines like terms in a polynomial
    polyDict = {}
    for term in poly:
        coeff, xpow, ypow = term
        if((xpow, ypow) in polyDict):
            polyDict[(xpow, ypow)] += coeff
        else:
            polyDict[(xpow, ypow)] = coeff
    return [[polyDict[powers], powers[0], powers[1]] for powers in polyDict]

def maclaurin(origPoly): #T3 using maclaurin series
    mcPoly = []
    print("maclaurin progress: ", end = '\r')
    mcPoly.extend(polyPow(origPoly, 0, 1/2)) #1/2
    print("maclaurin progress: finished 0th power", end = '\r')
    mcPoly.extend(polyPow(origPoly, 1, 1/4)) #+1/4x
    print("maclaurin progress: finished 1st power", end = '\r')
    mcPoly.extend(polyPow(origPoly, 3, -1/48)) #-1/48x^2
    print("maclaurin progress: finished 3rd power", end = '\r')
    mcPoly.extend(polyPow(origPoly, 5, 1/480)) #+1/480x^5
    print("maclaurin progress: finished 5th power", end = '\r')
    mcPoly.extend(polyPow(origPoly, 7, -17/80640)) #-17/80640x^7
    print("maclaurin progress: finished 7th power", end = '\r')
    return(polycomb(mcPoly))

layer = [x.copy() for x in inputLayer]

print("first layer of size {}".format(layerCts[0]))
for node in layer:
    polyprint(node)
print()

for k in range(len(layerCts)-2):
    layerOutput = []
    for start in range(0, len(weights[k]), layerCts[k]):
        nodeOutput = []
        for i,weight in enumerate(weights[k][start:start+layerCts[k]]):
            for term in layer[i]:
                nodeOutput.append([term[0]*weight, term[1], term[2]])
        layerOutput.append(polycomb(nodeOutput))

    print("starting maclaurin to output layer {} of size {}".format(k+2, layerCts[k+1]))
    layer = [maclaurin(node) for node in layerOutput]

    for node in layer:
        polyprint(node)
    print()

print("output for last layer")
for node in layer:
    for term in node:
        term[0] *= weights[-1][0]
    polyprint(node)
