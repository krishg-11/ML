from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from PIL import Image

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ImageName = "chess.jpg"
img = Image.open(ImageName)
pix = img.load()

r = []
g = []
b = []
for x in range(img.size[0]):
    for y in range(img.size[1]):
        r.append(pix[x,y][0])
        g.append(pix[x,y][1])
        b.append(pix[x,y][2])


ax.scatter(r, g, b, c='r', marker='.')

ax.set_xlabel('R Label')
ax.set_ylabel('G Label')
ax.set_zlabel('B Label')

plt.show()
