from random import choice
from collections import OrderedDict, defaultdict

class PolygonSet:

    def __init__(self, tile_set, node_set: 'NodeSet', edge_set: 'EdgeSet'):
        self.min_angle = min(sum(map(lambda x: x.angles, tile_set), []))
        self.node_set = node_set
        self.edge_set = edge_set
        self.open_edges = OrderedDict()
        self.hidden_open_edge = {}
        self.children_of = {}
        self.parent_of = {}

    def get_random_open_edge(self):
        return choice(list(self.open_edges.keys()))

    def get_fifo_open_edge(self):
        return next(iter(self.open_edges))

    def remove_polygon(self, edge: 'Edge' = None, polygon: 'Polygon' = None):
        if edge != None:
            polygon = self.open_edges[edge]

        #remove children
        if polygon in self.children_of:
            for child in self.children_of[polygon]:
                self.remove_polygon(polygon=child)
            self.children_of.pop(polygon)
        
        #remove self
        closed_angles_to_remove = defaultdict(list)
        for edge in polygon.edges:
            if edge in self.open_edges.keys():
                self.open_edges.pop(edge)
                self.edge_set.try_remove(edge)

                closed_angles_to_remove[edge.node2].append(edge.relative_angle)
                closed_angles_to_remove[edge.node1].append(edge.reverse_relative_angle)
            else:
                self.unhide(edge)

                closed_angles_to_remove[edge.node1].append(edge.relative_angle)
                closed_angles_to_remove[edge.node2].append(edge.reverse_relative_angle)

        for node in closed_angles_to_remove.keys():
            if len(node.closed_angles) == 1:
                self.node_set.remove(node)
            else:
                node.closed_angles.remove(closed_angles_to_remove[node])
                
        #remove child parent relationship if not root
        if polygon in self.parent_of:
            self.parent_of.pop(polygon)  

    def add_parent_child(self, parent: 'Polygon', child: 'Polygon'):
        if parent not in self.children_of.keys():
            self.children_of[parent] = [child]
        else:
            self.children_of[parent].append(child)

        self.parent_of[child] = parent

    def hide(self, edge: 'Edge'):
        self.hidden_open_edge[edge] = self.open_edges[edge]
        self.open_edges.pop(edge)

    def unhide(self, edge: 'Edge'):
        self.open_edges[edge] = self.hidden_open_edge[edge]
        self.hidden_open_edge.pop(edge)