from random import choice, shuffle
from PolygonTypes import *
from NodeSet import NodeSet
from EdgeSet import EdgeSet
from PolygonSet import PolygonSet

class TilingEngine:

	def __init__(self):
		self.polygon_graph = {}
		self.reverse_graph = {}

	# Constructs a graph of vertices and edges of type Polygon and Edge 
	# respectivly.
	@staticmethod
	def tile(tile_set = [Bowtie, Decagon, Hexagon, Pentagon, Rhombus], radial_placement = True):
		node_set = NodeSet(100)
		edge_set = EdgeSet(1000, 1000, node_set)
		polygon_set = PolygonSet(node_set, edge_set)

		InitPolygonType = choice(tile_set)
		Polygon.create(InitPolygonType, polygon_set)
		for _ in range(1):
			cur_edge = polygon_set.get_random_open_edge()
			#possible to switch next line with generator function?
			possibilities = [(PolygonType, i) for PolygonType in tile_set for i in range(len(PolygonType.angles))]
			shuffle(possibilities)
			for possibility in possibilities:
				NewPolygonType, start_index = possibility
				valid_new_edges = Polygon.place(NewPolygonType, cur_edge, start_index, polygon_set)
				if valid_new_edges != None:
					NewPolygonType(valid_new_edges, polygon_set)
					break

			polygon_set.remove_polygon_ref_by_edge(cur_edge)