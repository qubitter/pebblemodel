from PIL import Image
from PIL import ImageFilter
import copy
import pandas as pd

dim = 255

stack = [(int((dim+1)/2), int((dim+1)/2))]

g = [[0 for j in range(dim)] for i in range(dim)]

g[int((dim+1)/2)][int((dim+1)/2)] = 8315

def topple(r, c):
    g[r][c] -= 4
    g[r-1][c] += 1
    stack.append((r-1, c))
    g[r+1][c] += 1
    stack.append((r+1, c))
    g[r][c+1] += 1
    stack.append((r, c+1))
    g[r][c-1] += 1
    stack.append((r, c-1))

count = 0
while len(stack) > 0:
    (r, c) = stack.pop(0)
    if g[r][c] >= 4:
        while g[r][c] >= 4:
            topple(r, c)
        img = Image.frombytes("RGB", (dim, dim), bytes([0 for i in range((dim**2)*3)]))
        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                mult = g[i][j]
                pixels[i, j] = (85*mult, 85*mult, 85*mult)

        img.save(str("0"*(5-(len(str(count)))))+str(count)+".png")
        count += 1

