import random, math, time

class Node:
    def __init__(self, name, neighbors, pebbles):
        self.name = name
        self.neighbors = neighbors
        self.pebbles = pebbles

    def get_name(self):
        return self.name

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        if self not in neighbor.get_neighbors():
            neighbor.add_neighbor(self)

    def is_neighboring(self, node):
        return (node in self.neighbors)

    def get_pebbles(self):
        return self.pebbles

    def set_pebbles(self, n):
        self.pebbles = n

    def incr_pebbles(self):
        self.pebbles += 1

    def is_toppled(self):
        return (len(self.neighbors) <= self.pebbles)

    def stabilize(self):
        for neighbor in self.neighbors:
            neighbor.incr_pebbles()
        self.pebbles -= len(self.neighbors)

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_toppled(self):
        return [node for node in self.nodes if node.is_toppled()]

    def get_nodes(self):
        return [node.get_name() + str(node.get_pebbles) for node in self.nodes]

    def __str__(self):
        return str({node.get_name():[[nb.get_name() for nb in node.get_neighbors()], node.get_pebbles()] for node in self.nodes})

def generate_tree(n):
    indices = [i for i in range(2, n+1)]
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    nodes = [seed_a, seed_b]
    for i in range(n-2):
        chosen = random.choice(nodes)
        new_node = Node(indices[i], [], 1)
        new_node.add_neighbor(chosen)
        nodes.append(new_node)

    return Graph(nodes)

def generate_cyclic(n):
    indices = [i for i in range(2, n+1)]
    seed_a = Node('0', [], 1)
    seed_b = Node('1', [], 1)
    seed_a.add_neighbor(seed_b)

    nodes = [seed_a, seed_b]
    for i in range(n-2):
        new_node = Node(indices[i], [], 1)
        new_node.add_neighbor(nodes[-1])
        nodes.append(new_node)

    return Graph(nodes)

def loop(g):
    if len(g.get_toppled()) == 0:
        return g
    else:
        for node in g.get_toppled():
            node.stabilize()
    loop(g)
