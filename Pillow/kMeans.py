'''
input: k-value image(file/url)
RGB values of each pixel as data set, group into k groups
replace each pixel with the rgb value of its nearest mean

K-Means:
1. Initialize centroids
2. categorize every data point to a centroid
3. Adjust centroid position

for each data point, know the rgb values

'''
import random
from PIL import Image
import urllib.request
import io
import sys
import time

global seen
global distances
distances = {}

def distance(p1, p2): #finds the distance between p1 and p2
    global distances
    if((p1,p2) not in distances):
        distances[(p1,p2)] = sum((p1[i]-p2[i])**2 for i in range(len(p1)))
    return distances[(p1,p2)]

def categorize(data, centroids): #given list of centroids and data, returns centroids dictionary
    categories = {i:[] for i in range(len(centroids))}

    centDistances = []
    for cent1 in range(len(centroids)):
        for cent2 in range(cent1+1, len(centroids)):
            centDistances.append(distance(centroids[cent1], centroids[cent2]))
    minCentDist = min(centDistances)/4

    seenRGB = {}
    for pixel in data:
        rgb = pixel[0]
        if(rgb in seenRGB):
            categories[seenRGB[rgb]].append(pixel)
            continue
        distances = []
        broken = False
        count = 0
        for cent in centroids:
            dist = distance(rgb, cent)
            distances.append((dist,count))
            if(dist < minCentDist):
                categories[count].append(pixel)
                seenRGB[rgb] = count
                broken = True
                break
            count += 1
        if(broken): continue
        closest = min(distances)[1]
        categories[closest].append(pixel)
        seenRGB[rgb] = closest
    return categories

def reposition(categories): #given centroids dictionary, returns centroid list of new positions
    newCentroids = []
    for cent in categories:
        pointDim = len(categories[cent][0][0]) # 3 since there are 3 channels (r,g,b)
        averages = tuple([sum(pixel[0][i] for pixel in categories[cent])/len(categories[cent]) for i in range(pointDim)])
        newCentroids.append(averages)
    return newCentroids

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

def initalizeCentroids(pixelNL, setPixelNL, count): #Better initialization method smh
    # # RANDOM
    # kcoords = set()
    # uniquePixelsNL = list(setPixelNL)
    # for i in range(count):
    #     add = random.choice(uniquePixelsNL)
    #     while(add in kcoords):
    #         add = random.choice(uniquePixelsNL)
    #     kcoords.add(add)
    # return list(kcoords)

    # KMEANS++
    uniquePixelsNL = list(setPixelNL) #make sure kcoords are unique
    kcoords = [pixelNL[int(random.random()*len(pixelNL))]]
    for i in range(count-1):
        # dists = [(min(distance(pixel, kcoord) for kcoord in kcoords), pixel) for pixel in uniquePixelsNL]
        # kcoords.append(max(dists)[1])
        dists =   [min(distance(pixel, kcoord) for kcoord in kcoords) for pixel in uniquePixelsNL]
        kcoords.append(random.choices(uniquePixelsNL, weights=dists)[0])
    return kcoords


start = time.time()
#take in input
for input in sys.argv[1:]:
    if(input.isnumeric()):
        k = int(input)
    else:
        imageInfo = input

if('http' in imageInfo):
    imageInfo = io.BytesIO(urllib.request.urlopen(imageInfo).read())
img = Image.open(imageInfo)
pix = img.load()

#set up data and centroids
pixels = [[pix[x,y], (x,y)] for x in range(img.size[0]) for y in range(img.size[1])]
pixelNoLocation = [(rgb[0],rgb[1],rgb[2]) for rgb,pos in pixels]
setPixelNL = set(pixelNoLocation)

print('size:', img.size[0], 'x', img.size[1])
print('pixels:', len(pixels))
print('distinct pixel count:', len(setPixelNL))
counts = {pixel:0 for pixel in setPixelNL}
for pixel in pixelNoLocation:
    counts[pixel] += 1
# mostCommon = max((pixelNoLocation.count(pixel), pixel) for pixel in setPixelNL)
mostCommon = max(counts, key=counts.get)
print('most common pixel:', mostCommon, '=>', counts[mostCommon])

kcoords = initalizeCentroids(pixelNoLocation, setPixelNL, k)
print('random means:', kcoords)
print("Centroids initialized; time taken so far", time.time()-start, end='\n\n')

categories = categorize(pixels, kcoords)

net = [len(categories[k]) for k in categories]
print('starting sizes', net)

count = 0
while(net != [0]*k):
    count += 1
    kcoords = reposition(categories)
    newCategories = categorize(pixels, kcoords)
    net = [len(newCategories[k]) - len(categories[k]) for k in categories]
    categories = newCategories
    print(f'diff {count}: {net} -- time taken:', time.time()-start)

print()
print('Final means:')
count = 0
for cent in categories:
    count+=1
    print(f'{count}: {tuple(kcoords[cent])} => {len(categories[cent])}')
    for point in categories[cent]:
        x,y = point[1]
        pix[x,y] = tuple([round(channel) for channel in kcoords[cent]])

img.save('kmeans/{}.png'.format('2021kganotra'), 'PNG')

kcoords = [(round(rgb[0]), round(rgb[1]), round(rgb[2])) for rgb in kcoords]
seen = set()
regionCount = {cent:0 for cent in kcoords}
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
