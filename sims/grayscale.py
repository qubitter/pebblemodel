from basicsim import *
from PIL import Image
import sys

sys.setrecursionlimit(5000)

g = generate_grid(100, 100, 0)

origin = g.get_nodes()[4750]

origin.set_pebbles(2500)

final = loop(g).get_nodes()

data = [node.get_pebbles() for node in final]
data = [[255*i//3,255*i//3,255*i//3] for i in data]
datum = []

for i in data: datum += i

print(datum)

data = bytes(datum)
img = Image.frombytes('RGB', (100, 100), data)


img.show()
