from PIL import Image
from PIL import ImageFilter
import copy
import pandas as pd
import imageio
import os
import math
import numpy
import random


def gradient(x):
    return (int(math.sin(2*math.pi*x+0*math.pi/3)*127)+128, int(math.sin(2*math.pi*x+2*math.pi/3)*127)+128, int(math.sin(2*math.pi*x+4*math.pi/3)*127)+128)

count = 0

images = []

dim = 101

init = 5000

maxwhite = init

queue = [(None, None), (int((dim-1)/2), int((dim-1)/2))]

g = [[0 for j in range(dim)] for i in range(dim)]

g[int((dim-1)/2)][int((dim-1)/2)] = maxwhite


def topple(r, c):
    g[r][c] -= 4

    g[r-1][c] += 1
    queue.append((r-1, c))
    g[r+1][c] += 1
    queue.append((r+1, c))
    g[r][c+1] += 1
    queue.append((r, c+1))
    g[r][c-1] += 1
    queue.append((r, c-1))

while len(queue) > 1:
    (r, c) = queue.pop(0)
    if (r, c) == (None, None):

        maxwhite = max([max(gg) for gg in g])
        print(maxwhite)

        img = Image.new("RGB", (dim,dim), color=0)

        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                mult = g[i][j]
                if mult > 0:
                    pixels[i, j] = gradient(mult/init)

        images.append(img)

        queue.append((None, None))

        count += 1


    else:
        while g[r][c] >= 4:
            topple(r, c)


for extras in range(50):

    images.append(img)


namer = str(random.randint(1, 999999))

img.save("final_state" + namer + ".png")



imageio.mimsave('/Users/simon/Downloads/pebblemodel-master/movie' + namer + '.gif', images)
