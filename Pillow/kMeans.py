import sys; args=sys.argv[1:]
#Krish Ganotra - kmeans rgb
import random
from PIL import Image
import time

global seen

def distance(p1, p2): #finds the distance between p1 and p2
    return sum((p1[i]-p2[i])**2 for i in range(len(p1)))

def categorize_and_reposition(rgbDict, centroids):
    centDistances = []
    for cent1 in range(len(centroids)):
        for cent2 in range(cent1+1, len(centroids)):
            centDistances.append(distance(centroids[cent1], centroids[cent2]))
    minCentDist = min(centDistances)/4

    centCounts = [0]*len(centroids)
    centSums = [[0,0,0] for i in range(len(centroids))]
    for rgb in rgbDict:
        closestCentInd = -1
        occurences, centInd = rgbDict[rgb]
        distances = [(distance(rgb, centroids[centInd]), centInd)]
        if(distances[0][0] < minCentDist):
            closestCentInd = centInd
        else:
            for icent, cent in enumerate(centroids):
                if(icent == centInd): continue
                dist = distance(cent, rgb)
                if(dist < minCentDist):
                    closestCentInd = icent
                    break
                distances.append((dist, icent))
        if(closestCentInd == -1):
            closestCentInd = min(distances)[1]

        rgbDict[rgb] = [occurences, closestCentInd]
        centCounts[closestCentInd] += occurences
        for i in range(3):
            centSums[closestCentInd][i] += occurences*rgb[i]
    new_centroids = []
    for centInd in range(len(centroids)):
        new_cent = tuple(centSums[centInd][i]/centCounts[centInd] for i in range(3))
        new_centroids.append(new_cent)
    return rgbDict, centCounts, new_centroids



# def reposition(rgbDict, k): #given rgb dictionary, returns centroid list of new positions
#     rgbLen = 3
#     centroids = [[0]*rgbLen]*k
#     centroidCounts = [0]*k
#     for rgb in rgbDict:
#         occurences, centInd = rgbDict[rgb]
#         centroids[centInd] = [centroids[centInd][i]+rgb[i]*occurences for i in range(rgbLen)]
#         centroidCounts[centInd] += occurences
#     return [tuple(centroids[centInd][i]/centroidCounts[centInd] for i in range(rgbLen)) for centInd in range(k)]


'''
{(rgb): [occurences, centroidIndex]}
[centroid1, centroid2,...]
'''

def areaFill(pix, x, y):
    global seen
    seen.add((x,y))
    queue = [(x,y)]
    while(queue):
        x,y = queue.pop(0)
        for deltax in [-1,0,1]:
            for deltay in [-1, 0, 1]:
                newx = x+deltax
                newy = y+deltay
                if((newx,newy) not in seen and newx>=0 and newx<img.size[0] and newy>=0 and newy<img.size[1] and pix[newx,newy]==pix[x,y]):
                    queue.append((newx,newy))
                    seen.add((newx,newy))

def initalizeCentroids(rgbDict, count):
    # kcoords = [random.choice(allrgb)]
    # prob = [distance(pixel, kcoords[0]) for pixel in allrgb]
    # for i in range(count-1):
    #     print(kcoords)
    #     kcoords.append(random.choices(population=allrgb, weights=prob)[0])
    #     prob = [min(distance(pixel, kcoords[i]) for i in range(len(kcoords))) for pixel in pixels]
    #
    # return kcoords

    allrgb = list(rgbDict.keys())
    kcoords = []
    for i in range(count):
        add = random.choice(allrgb)
        while(add in kcoords):
            add = random.choice(allrgb)
        kcoords.append(add)
    return kcoords


start = time.time()
#take in input
for input in sys.argv[1:]:
    if(input.isnumeric()):
        k = int(input)
    else:
        imageInfo = input

img = Image.open(imageInfo)
pix = img.load()

#set up data and centroids
rgbDict = {}
for x in range(img.size[0]):
    for y in range(img.size[1]):
        rgb = pix[x,y]
        if(rgb in rgbDict): rgbDict[rgb][0] += 1
        else: rgbDict[rgb] = [1, 0]

print('size:', img.size[0], 'x', img.size[1])
print('pixels:', img.size[0]*img.size[1])
print('distinct pixel count:', len(rgbDict))
mostCommon = max((rgbDict[rgb][0], rgb) for rgb in rgbDict)
print('most common pixel:', mostCommon[1], '=>', mostCommon[0])

centroids = initalizeCentroids(rgbDict, k)
# print('random means:', centroids, end='\n\n')

count = 0
centCounts = [0]*k
net = []
while(net != [0]*k):
    count += 1
    rgbDict, newCentCounts, centroids = categorize_and_reposition(rgbDict, centroids)
    net = [newCentCounts[i]-centCounts[i] for i in range(len(centCounts))]
    centCounts = newCentCounts
    # print(f'diff {count}: {net}-- time taken: {time.time()-start}')

print()
print('Final means:')
for i,cent in enumerate(centroids):
    print(f'{i+1}: {cent} => {centCounts[i]}')

centroids = [tuple(round(cent[i]) for i in range(3)) for cent in centroids]
for x in range(img.size[0]):
    for y in range(img.size[1]):
        currRGB = pix[x,y]
        newRGB = centroids[rgbDict[currRGB][1]]
        pix[x,y] = newRGB


img.save('kmeans/{}.png'.format('2021kganotra'), 'PNG')

seen = set()
regionCount = {cent:0 for cent in centroids}
print()
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if((x,y) in seen): continue
        areaFill(pix, x, y)
        regionCount[pix[x,y]] += 1

print('Region counts: ', end='')
count = 0
print(', '.join([str(x) for x in regionCount.values()]))


print('total time:', time.time()-start)
#img.show()
