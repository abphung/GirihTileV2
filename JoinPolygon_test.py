import unittest
from RenderingEngineMatplotlib import RenderingEngineMatplotlib
from PolygonTypes import *
from NodeSet import NodeSet
from EdgeSet import EdgeSet
from PolygonSet import PolygonSet
import sys

class JoinPolygonUnitTests(unittest.TestCase):

	def test_simple_shapes(self):
		for PolygonType in [Bowtie, Decagon, Hexagon, Pentagon, Rhombus]:
			self.perform_test_n([PolygonType], [], [6], True)

	def test_hexagon_hexagon(self):
		self.perform_test_n([Hexagon, Hexagon], [(0, 0, 0)], [len(Hexagon.angles) - 1, len(Hexagon.angles) - 1], True)

	#angle too small
	def test_bowtie_hexagon_pentagon(self):
		self.perform_test_n([Bowtie, Hexagon, Pentagon], [(0, 2, 0), (1, 4, 0)], None, False)

	def test_decagon_bowtie(self):
		self.perform_test_n([Decagon, Bowtie], [(0, 5, 0)], [8, 4], True)

	def test_decagon_hexagon_hexagon_bowtie(self):
		self.perform_test_n([Decagon, Hexagon, Hexagon, Bowtie], [(0, 0, 0), (0, 2, 1), (0, 1, 1)], [7, 3, 3, 1], True)

	def test_pentagon_hexagon_decagon(self):
		self.perform_test_n([Pentagon, Hexagon, Decagon], [(0, 0, 0), (1, 4, 0)], None, False)

	def test_pentagron_rhombus_pentagon_decagon_bowtie(self):
		self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (2, 0, 1)], [], False)
		self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (1, 2, 2)], [], False)

	#overlap
	def test_decagon_decagon_decagon(self):
		self.perform_test_n([Decagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False)

	def test_pentagon_decagon_decagon(self):
		self.perform_test_n([Pentagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False)

	def test_decagon_bowtie_pentagon(self):
		self.perform_test_n([Decagon, Bowtie, Pentagon], [(0, 0, 0), (0, 2, 0)], [], False)

	def test_bowtie_bowtie_bowtie(self):
		self.perform_test_n([Bowtie, Bowtie, Bowtie], [(0, 0, 0), (0, 2, 4)], [], True)

	def perform_test_n(self, polygon_types, joining_edges_collection, polygons_open_count, valid):
		gettrace = getattr(sys, 'gettrace', None)
		is_debug = gettrace is not None and gettrace()

		tile_set = [Bowtie, Decagon, Hexagon, Pentagon, Rhombus]
		node_set = NodeSet(100)
		edge_set = EdgeSet(1000, 1000, node_set)
		polygon_set = PolygonSet(tile_set, node_set, edge_set)
		polygons = [Polygon.create(polygon_types[0], polygon_set)]
		renderingEngine = RenderingEngineMatplotlib(1000, 1000)
		is_invalid_edge_present = False
		for PolygonType in polygon_types[1:]:
			polygon1_index, polygon1_side_index, polygon2_side_index = joining_edges_collection.pop(0)
			valid_new_edges = Polygon.place(PolygonType, polygons[polygon1_index].edges[polygon1_side_index], polygon2_side_index, polygon_set, allow_collisions=is_debug)
			if valid_new_edges == None:
				is_invalid_edge_present = True
				break
			polygons.append(PolygonType(valid_new_edges, polygon_set))

		
		if is_debug:
			renderingEngine.draw(polygons)

		if valid:
			self.assertEqual(len(polygons), len(polygon_types))
			# for i, open_count in enumerate(polygons_open_count):
			# 	self.assertEqual(len(polygons[i].open_edges), open_count)
		else:
			self.assertTrue(is_invalid_edge_present)

		return polygons

if __name__ == '__main__':
    unittest.main()