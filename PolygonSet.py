from random import choice

class PolygonSet:

    def __init__(self, node_set: 'NodeSet', edge_set: 'EdgeSet'):
        self.node_set = node_set
        self.edge_set = edge_set
        self.open_edges = {}

    def get_random_open_edge(self):
        return choice(list(self.open_edges.keys()))

    def remove_polygon_ref_by_edge(self, edge: 'Edge'):
        pass
