from Node import Node
from typing import List
from math import *

class Edge:

	@staticmethod
	def create(node1: Node, node2: Node, edge_set: 'EdgeSet' = None) -> [bool, 'Edge']:
		existing_edge = edge_set.try_get(node1, node2)
		if existing_edge != None:
			return (False, existing_edge)
		new_edge = Edge(node1, node2)
		return (True, new_edge)

	# edges are pointed so that polygon1 is on the left and polygon2 is on the right
	def __init__(self, node1: 'Node', node2: 'Node'):
		self.node1 = node1
		self.node2 = node2
		self.reversed = False
		self.open = True
		self.color = None
		self.polygon1 = None
		self.polygon2 = None

	# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
	def ccw(A: 'Node', B: 'Node', C: 'Node') -> bool:
		return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

	def intersects(self, other_edge: 'Edge'):
		if self is other_edge or sum([self.node1 == other_edge.node2, self.node2 == other_edge.node1, self.node1 == other_edge.node1, self.node2 == other_edge.node2]) == 1:
			return False
		does_intersect = Edge.ccw(self.node1, other_edge.node1, other_edge.node2) != Edge.ccw(self.node2, other_edge.node1, other_edge.node2) and \
			Edge.ccw(self.node1, self.node2, other_edge.node1) != Edge.ccw(self.node1, self.node2, other_edge.node2)

		return does_intersect

	#returns int in range [0, 360]
	def angle(self):
		# instead of doing node1 - node2 do node2 - node1 + 180 so all angles are positive
		return round(degrees(atan2(self.node1.y - self.node2.y, self.node1.x - self.node2.x)) + 180)

	def reverse(self):
		self.reversed = not self.reversed
		self.node1, self.node2 = self.node2, self.node1

	def close(self):
		self.open = False

	def __str__(self):
		return str((self.node1, self.node2))

	def __repr__(self):
		return self.__str__()