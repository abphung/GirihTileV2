import unittest
from RenderingEngineMatplotlib import RenderingEngineMatplotlib
from PolygonTypes import *
from NodeSet import NodeSet
from EdgeSet import EdgeSet
from PolygonSet import PolygonSet
import sys

class PolygonSetUnitTests(unittest.TestCase):
	
	def test_remove_single(self):
		# gettrace = getattr(sys, 'gettrace', None)
		# is_debug = gettrace is not None and gettrace()

		tile_set = [Bowtie, Decagon, Hexagon, Pentagon, Rhombus]
		
		for PolygonType in tile_set:
			node_set = NodeSet(100)
			edge_set = EdgeSet(1000, 1000, node_set)
			polygon_set = PolygonSet(tile_set, node_set, edge_set)
			polygon = Polygon.create(PolygonType, polygon_set)

			self.assertNotEqual(len(polygon_set.open_edges), 0)
			self.assertNotEqual(len(node_set.nodes.keys()), 0)
			self.assertNotEqual(len(node_set.locations), 0)
			self.assertNotEqual(len(edge_set.edges.keys()), 0)

			polygon_set.remove_polygon(polygon=polygon)

			self.assertEqual(len(polygon_set.open_edges), 0)
			self.assertEqual(len(node_set.nodes.keys()), 0)
			self.assertEqual(len(node_set.locations), 0)
			self.assertEqual(len(edge_set.edges.keys()), 0)

if __name__ == '__main__':
	unittest.main()