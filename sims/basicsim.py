import random
from tools import ncr


class Node:
    def __init__(self, name, neighbors, pebbles, type="normal"):
        self.name = name
        self.neighbors = neighbors
        self.pebbles = pebbles
        self.type = type # To check if node is a sink or a normal vertex
        self.toppled = 0

    def __str__(self):
        return f"[{self.name}: {[n.get_name() for n in self.neighbors]}, {self.pebbles}]"

    def get_name(self):
        return self.name

    def get_neighbors(self):
        return self.neighbors

    def neighbors_to_str(self):
        return str(list(map(lambda x: x.get_name(), self.neighbors)))

    def add_neighbor(self, neighbor): #so we can build graphs non-self-referentially
        self.neighbors.append(neighbor)
        if self not in neighbor.get_neighbors():
            neighbor.add_neighbor(self)

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            nbs = set(self.neighbors)
            nbs -= {neighbor}
            self.neighbors = list(nbs)
            neighbor.remove_neighbor(self)

    def is_neighboring(self, node):
        return (node in self.neighbors)

    def get_pebbles(self):
        return self.pebbles

    def set_pebbles(self, n):
        self.pebbles = n

    def incr_pebbles(self):
        self.pebbles += 1

    def is_unstable(self):
        return (len(self.neighbors) <= 4) # <= self.pebbles

    def get_toppled(self):
        return self.toppled

    def topple(self): #easier here
        if self.type=="normal":
            for neighbor in self.neighbors:
                neighbor.incr_pebbles()
            self.pebbles -= len(self.neighbors)
            self.toppled += 1

    def get_new_neighbors(self, nodes, num_neighbors):

        def new_neighbor(node):
            if not self.is_neighboring(node): return node
            return new_neighbor(random.choice(nodes))

        for i in range(num_neighbors):
            new_node = new_neighbor(random.choice(nodes))
            self.add_neighbor(new_node)

class Graph:
    def __init__(self, nodes, sink=None):
        self.nodes = nodes
        self.sink = sink
        if not sink: self.sink = Node("sink", [], 0)

    def unstable(self):
        return [node for node in self.nodes if node.is_unstable()]

    def get_nodes(self):
        return self.nodes

    def get_sink(self):
        return self.sink

    def has_sink(self):
        if self.sink.get_neighbors(): return True
        return False

    def __str__(self): #representation function for "pretty" printing
        return str([node.get_pebbles() for node in self.nodes]) + ", " + str([[n.get_name() for n in node.get_neighbors()] for node in self.nodes])
        # Add sink neighbors list

# Decorator that adds sink (keyword is sink_neighbors, which is the number of vertices that  the sink is connected to)
# to a function that generates a graph (it will look like you're adding an
# "Unexpected Keyword Argument" when you call the function, but this is fine)
def sink(func):
    def wrapper(*args, **kwargs):
        sink_neighbors = kwargs.pop("sink_neighbors", 0)
        g = func(*args, **kwargs)
        sink = g.get_sink()
        nodes = g.get_nodes()
        sink.get_new_neighbors(nodes, sink_neighbors)
        return g
    return wrapper

@sink
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

@sink
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

@sink
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
    indices = [i for i in range(2, l)]
    seed_a = Node('0', [], 0)
    seed_b = Node('1', [], 0)
    seed_a.add_neighbor(seed_b)

    rnodes = [seed_a, seed_b]

    allnodes = [rnodes]

    for i in indices:
        new = Node(str(i), [], 0)
        rnodes[-1].add_neighbor(new)
        rnodes.append(new)

    for row in range(1, w):
        indices = [i for i in range(2, l)]
        seed_a = Node('0', [], 0)
        seed_b = Node('1', [], 0)
        seed_a.add_neighbor(seed_b)

        seed_a.add_neighbor(allnodes[row-1][0])
        seed_b.add_neighbor(allnodes[row-1][1])

        thisrow = [seed_a, seed_b]

        for i in indices:
            new = Node(str(i), [], 0)
            thisrow[-1].add_neighbor(new)
            new.add_neighbor(allnodes[row-1][i])
            thisrow.append(new)

        allnodes.append(thisrow)

    out = []

    for i in allnodes: out += i

    for i in range(pebbles): random.choice(out).incr_pebbles()

    return Graph(out)


@sink
def generate_bipartite(num_a, num_b, num_pebbles, num_edges=None):
    if not num_edges: num_edges = random.randint(0, num_a * num_b + 1)
    nodes_a = []
    nodes_b = []

    for i in range(num_a):
        new_node = Node(f"a_{i}", [], 0)
        nodes_a.append(new_node)

    for i in range(num_b):
        new_node = Node(f"b_{i}", [], 0)
        neighbor = random.choice(nodes_a)
        new_node.add_neighbor(neighbor)
        nodes_b.append(new_node)
    num_edges -= num_b

    for node in nodes_a:
        if not node.neighbors:
            node.add_neighbor(random.choice(nodes_b))
    num_edges -= num_a

    for i in range(num_edges):
        random.choice(nodes_a).get_new_neighbors(nodes_b, 1)

    nodes = nodes_a + nodes_b

    for i in range(num_pebbles):
        random.choice(nodes).incr_pebbles()

    return Graph(nodes)

def generate_random(n, pebbles):
    nodes = [Node(str(i), [], 0) for i in range(n)]
    edges = 0
    for node in nodes:
        for neighbor in nodes:
            if neighbor not in node.get_neighbors():
                if node not in neighbor.get_neighbors():
                    if random.uniform(0, 1) > 0.5:
                        node.add_neighbor(neighbor)
                        edges += 1
    for i in range(edges-pebbles): random.choice(nodes).incr_pebbles()

    return Graph(nodes)


def loop(g, iter = 0):
    print("Looping!")
    while True:
        stillworking = False
        iter += 1
        biter = 0
        l = len(g.unstable())
        for node in g.unstable():
            biter += 1
            print(f"Toppling node {biter} of {l}; iteration {iter}", end="\r")
            stillworking = True
            node.topple()
        if not stillworking:
            print(f"Graph is stable after {iter} iterations.")
            return g


if __name__ == '__main__':
    for i in range(3, 100):
        try:
            g = loop(generate_random(i, -10))
            # print(f"{i}: {True}; {[node.get_toppled() for node in g.get_nodes()]}; {[node.__str__() for node in g.get_nodes()]}")
            print(f"{i}: {True}")
        except RuntimeError:
            print(f"{i}: {False}")
