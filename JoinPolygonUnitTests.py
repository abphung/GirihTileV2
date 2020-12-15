import unittest
from RenderingEngine import RenderingEngine
from PolygonTypes import *
from NodeSet import NodeSet
from EdgeSet import EdgeSet

class JoinPolygonUnitTests(unittest.TestCase):

	# def test_hexagon(self):
	# 	polygons = self.perform_test_n([Hexagon], [], [6], True, False)

	# def test_hexagon_hexagon(self):
	# 	self.perform_test_n([Hexagon, Hexagon], [(0, 0, 0)], [len(Hexagon.angles) - 1, len(Hexagon.angles) - 1], True, False)

	# def test_bowtie_hexagon_pentagon(self):
	# 	self.perform_test_n([Bowtie, Hexagon, Pentagon], [(0, 2, 0), (1, 4, 0)], None, False, False)

	# def test_decagon_bowtie(self):
	# 	self.perform_test_n([Decagon, Bowtie], [(0, 5, 0)], [8, 4], True, False)

	# def test_decagon_hexagon_hexagon_bowtie(self):
	# 	self.perform_test_n([Decagon, Hexagon, Hexagon, Bowtie], [(0, 0, 0), (0, 2, 1), (0, 1, 1)], [7, 3, 3, 1], True, False)

	# def test_pentagon_hexagon_decagon(self):
	# 	self.perform_test_n([Pentagon, Hexagon, Decagon], [(0, 0, 0), (1, 4, 0)], None, False, False)

	# def test_pentagron_rhombus_pentagon_decagon_bowtie(self):
	# 	self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (2, 0, 1)], [], False, False)
	# 	self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (1, 2, 2)], [], False, False)

	# def test_decagon_decagon_decagon(self):
	# 	self.perform_test_n([Decagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False, False)

	def test_pentagon_decagon_decagon(self):
		self.perform_test_n([Pentagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False, True)

	# def test_decagon_bowtie_pentagon(self):
	# 	self.perform_test_n([Decagon, Bowtie, Pentagon], [(0, 0, 0), (0, 2, 0)], [], False, False)

	# def test_bowtie_bowtie_bowtie(self):
	# 	self.perform_test_n([Decagon, Bowtie, Pentagon], [(0, 0, 0), (0, 2, 0)], [], False, False)

	def perform_test_n(self, polygon_types, joining_edges_collection, polygons_open_count, valid, should_draw):
		node_set = NodeSet(100)
		edge_set = EdgeSet(1000, 1000, node_set)
		polygons = [Polygon.create(polygon_types[0], node_set, edge_set)]
		renderingEngine = RenderingEngine(1000, 1000)
		is_invalid_edge_present = False
		for PolygonType in polygon_types[1:]:
			polygon1_index, polygon1_side_index, polygon2_side_index = joining_edges_collection.pop(0)
			joining_edges, valid_new_edges = Polygon.place(PolygonType, polygons[polygon1_index].edges[polygon1_side_index], polygon2_side_index, node_set, edge_set)
			if valid_new_edges == None:
				is_invalid_edge_present = True
				break
			polygons.append(PolygonType(joining_edges, valid_new_edges, node_set, edge_set))

		if should_draw:
			renderingEngine.draw(polygons)

		if valid:
			self.assertEqual(len(polygons), len(polygon_types))
			for i, open_count in enumerate(polygons_open_count):
				self.assertEqual(len(polygons[i].open_edges), open_count)
		else:
			self.assertTrue(is_invalid_edge_present)

		return polygons

if __name__ == '__main__':
    unittest.main()