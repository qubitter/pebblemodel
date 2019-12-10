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

    def add_neighbor(self, neighbor): #so we can build graphs non-self-referentially
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

    def is_unstable(self):
        return (len(self.neighbors) <= self.pebbles)

    def topple(self): #easier here
        for neighbor in self.neighbors:
            neighbor.incr_pebbles()
        self.pebbles -= len(self.neighbors)

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    def unstable(self):
        return [node for node in self.nodes if node.is_unstable()]

    def get_nodes(self):
        return self.nodes

    def __str__(self): #representation function for "pretty" printing
        return str({node.get_name():[[nb.get_name() for nb in node.get_neighbors()], node.get_pebbles()] for node in self.nodes})

def generate_tree(n, pebbles, seed = None): #acyclic graph; seed is if we want to fold something in
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    if seed == None:
        nodes = [seed_a, seed_b]
    else:
        nodes = seed.get_nodes()

    indices = [i for i in range(len(nodes), n)]

    for i in range(n-2):
        chosen = random.choice(nodes)
        new_node = Node(str(indices[i]), [], 0)
        new_node.add_neighbor(chosen)
        nodes.append(new_node)

    for i in range(pebbles):
        random.choice(nodes).incr_pebbles()

    return Graph(nodes)

def generate_cyclic(n, pebbles): #circular cyclic graph
    indices = [i for i in range(2, n)]
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    nodes = [seed_a, seed_b]
    for i in range(n-2):
        new_node = Node(str(indices[i]), [], 0)
        new_node.add_neighbor(nodes[-1])
        nodes.append(new_node)
    nodes[-1].add_neighbor(seed_a)

    for i in range(pebbles):
        random.choice(nodes).incr_pebbles()

    return Graph(nodes)

def generate_complete(n, pebbles):
    indices = [i for i in range(2, n)]
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    nodes = [seed_a, seed_b]

    for i in range(n-2):
        new_node = Node(str(indices[i]), [], 0)
        for node in nodes: new_node.add_neighbor(node)
        nodes.append(new_node)

    for i in range(pebbles):
        random.choice(nodes).incr_pebbles()

    return Graph(nodes)

def generate_grid(l, w, pebbles):
    indices = [i for i in range(2, n)]
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    nodes = [seed_a, seed_b]

def loop(g):
    if len(g.unstable()) == 0:
        return True
    else:
        for node in g.unstable():
            node.topple()
        return loop(g)

for i in range(3, 100):
    print(f"{i}: {loop(generate_tree(i, i-2))}")
