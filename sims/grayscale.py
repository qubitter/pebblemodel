from basicsim import *
from PIL import Image
import sys

sys.setrecursionlimit(32768)

g = generate_grid(101, 101, 0)

origin = g.get_nodes()[5101]

origin.set_pebbles(8000)

final = loop(g).get_nodes()


data = [node.get_pebbles() for node in final]

print(sum(data))

data = [[255*i//3,255*i//3,255*i//3] for i in data]
datum = []

for i in data: datum += i

data = bytes(datum)
img = Image.frombytes('RGB', (101, 101), data)


img.show()
