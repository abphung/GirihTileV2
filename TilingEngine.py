from random import *
from PolygonTypes import *
from NodeSet import NodeSet
from EdgeSet import EdgeSet

class TilingEngine:

	# Constructs a graph of vertices and edges of type Polygon and Edge 
	# respectivly.
	@staticmethod
	def tile(tile_set = [Bowtie, Decagon, Hexagon, Pentagon, Rhombus], radial_placement = True):
		polygons = []
		node_set = NodeSet(100)
		edge_set = EdgeSet(1000, 1000, node_set)

		InitPolygonType = choice(tile_set)
		init_polygon = Polygon.create(InitPolygonType, node_set, edge_set)
		polygons.append(init_polygon)
		open_polygons = [init_polygon]
		for i in range(0):
			cur_polygon = open_polygons.pop(0)
			while cur_polygon.open_edges == []:
				cur_polygon = open_polygons.pop(0)
			while cur_polygon.open_edges != []:
				cur_edge = cur_polygon.get_open_edge()
				possibilities = [(PolygonType, i) for PolygonType in tile_set for i in range(len(PolygonType.angles))]
				shuffle(possibilities)
				found_valid_polygon = False
				for possibility in possibilities:
					NewPolygonType, start_index = possibility
					joining_edges, valid_new_edges = Polygon.place(NewPolygonType, cur_edge, start_index)
					if valid_new_edges != None:
						new_polygon = NewPolygonType(joining_edges, valid_new_edges)
						polygons.append(new_polygon)
						open_polygons.append(new_polygon)
						found_valid_polygon = True
						break
				if not found_valid_polygon:
					cur_polygon.open_edges.remove(cur_edge)

			if cur_polygon.open_edges != []:
				open_polygons.append(cur_polygon)
		return polygons