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

def distance(p1, p2): #finds the distance between p1 and p2
    return sum((p1[i]-p2[i])**2 for i in range(len(p1)))

def categorize(data, centroids): #given list of centroids and data, returns centroids dictionary
    categories = {i:[] for i in range(len(centroids))}

    centDistances = []
    for cent1 in range(len(centroids)):
        for cent2 in range(cent1+1, len(centroids)):
            centDistances.append(distance(centroids[cent1], centroids[cent2]))
    minCentDist = min(centDistances)/4

    for pixel in data:
        rgb = pixel[0]
        distances = []
        broken = False
        for cent in centroids:
            dist = distance(rgb, cent)
            distances.append(dist)
            if(dist < minCentDist):
                categories[len(distances)-1].append(pixel)
                broken = True
                break
        if(broken): continue
        closest = min([(dist,pos) for pos,dist in enumerate(distances)])[1]
        categories[closest].append(pixel)
    return categories

def reposition(categories): #given centroids dictionary, returns centroid list of new positions
    newCentroids = []
    for cent in categories:
        sums = [0 for i in range(len(categories[cent][0][0]))]
        total = 0
        for pixel in categories[cent]:
            rgb = pixel[0]
            for i in range(len(rgb)):
                sums[i]+=rgb[i]
            total+=1
        averages = [sum/total for sum in sums]
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

def initalizeCentroids(pixels, count):
    kcoords = []
    for i in range(count):
        add = random.choice(pixels)
        while(add in kcoords):
            add = random.choice(pixels)
        kcoords.append(add)
    return kcoords


    # kcoords = [random.choice(pixels)]
    # prob = [distance(pixel, kcoords[0]) for pixel in pixels]
    # for i in range(count-1):
    #     print(kcoords)
    #     kcoords.append(random.choices(population=pixels, weights=prob)[0])
    #     prob = [min(distance(pixel, kcoords[i]) for i in range(len(kcoords))) for pixel in pixels]
    #
    # return kcoords


start = time.time()
#take in input
for input in sys.argv[1:]:
    if(input.isnumeric()):
        k = int(input)
    else:
        imageInfo = input

if("http" in imageInfo):
    imageInfo = io.BytesIO(urllib.request.urlopen(imageInfo).read())
img = Image.open(imageInfo)
pix = img.load()

#set up data and centroids
pixels = [[pix[x,y], (x,y)] for x in range(img.size[0]) for y in range(img.size[1])]
pixelNoLocation = [(rgb[0],rgb[1],rgb[2]) for rgb,pos in pixels]
setPixelNL = set(pixelNoLocation)

print("size:", img.size[0], "x", img.size[1])
print("pixels:", len(pixels))
print("distinct pixel count:", len(setPixelNL))
counts = {pixel:0 for pixel in setPixelNL}
for pixel in pixelNoLocation:
    counts[pixel] += 1
# mostCommon = max((pixelNoLocation.count(pixel), pixel) for pixel in setPixelNL)
mostCommon = max(counts, key=counts.get)
print("most common pixel:", mostCommon, "=>", counts[mostCommon])

kcoords = initalizeCentroids(pixelNoLocation, k)
print("random means:", kcoords, end="\n\n")

categories = categorize(pixels, kcoords)
net = [len(categories[k]) for k in categories]
print("starting sizes", net)

count = 0
while(net != [0]*k):
    count += 1
    kcoords = reposition(categories)
    newCategories = categorize(pixels, kcoords)
    net = [len(newCategories[k]) - len(categories[k]) for k in categories]
    categories = newCategories
    print("diff {}: {}".format(count,net))

print()
print("Final means:")
count = 0
for cent in categories:
    count+=1
    print("{}: {} => {}".format(count,tuple(kcoords[cent]),len(categories[cent])))
    for point in categories[cent]:
        x,y = point[1]
        pix[x,y] = tuple([round(x) for x in kcoords[cent]])

img.save("kmeans/{}.png".format("2021kganotra"), "PNG")

kcoords = [(round(rgb[0]), round(rgb[1]), round(rgb[2])) for rgb in kcoords]
seen = set()
regionCount = {cent:0 for cent in kcoords}
print()
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if((x,y) in seen): continue
        areaFill(pix, x, y)
        regionCount[pix[x,y]] += 1

print("Region counts: ", end="")
count = 0
print(", ".join([str(x) for x in regionCount.values()]))


print("total time:", time.time()-start)
#img.show()
