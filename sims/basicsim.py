import random, math, time

class Node:
    def __init__(self, graph, neighbors, pebbles):
        self.graph = graph
        self.neighbors = neighbors
        self.pebbles = pebbles

    def get_neighbors(self):
        return self.neighbors

    def is_neighboring(self, node):
        return (node in self.neighbors)

    def get_pebbles(self):
        return self.pebbles

    def is_toppled(self):
        return (len(self.neighbors) <= self.pebbles)

class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_toppled(self):
        return [node for node in self.nodes if node.is_toppled()]

    
