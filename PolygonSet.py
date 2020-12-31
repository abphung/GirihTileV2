from random import choice

class PolygonSet:

    def __init__(self, tile_set, node_set: 'NodeSet', edge_set: 'EdgeSet'):
        self.min_angle = min(sum(map(lambda x: x.angles, tile_set), []))
        self.node_set = node_set
        self.edge_set = edge_set
        self.open_edges = {}
        self.pop_source = {}

    def get_random_open_edge(self):
        return choice(list(self.open_edges.keys()))

    def remove_polygon_ref_by_edge(self, edge: 'Edge'):
        pass