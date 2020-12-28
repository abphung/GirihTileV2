from Node import Node
from typing import List
from math import degrees, atan2
class Edge:

	@staticmethod	
	def create(node1: Node, node2: Node, edge_set: 'EdgeSet' = None) -> [bool, 'Edge']:
		existing_edge = edge_set.try_get(node1, node2)
		if existing_edge != None:
			return (False, existing_edge)
		new_edge = Edge(node1, node2)
		return (True, new_edge)

	def __init__(self, node1: 'Node', node2: 'Node'):
		self.node1 = node1
		self.node2 = node2
		self.color = None
		self.relative_angle = round(degrees(atan2(self.node1.y - self.node2.y, self.node1.x - self.node2.x)))%360

	# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
	@staticmethod
	def ccw(A: 'Node', B: 'Node', C: 'Node') -> bool:
		return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

	def intersects(self, other_edge: 'Edge'):
		if self is other_edge or sum([self.node1 == other_edge.node2, self.node2 == other_edge.node1, self.node1 == other_edge.node1, self.node2 == other_edge.node2]) == 1:
			return False
		does_intersect = Edge.ccw(self.node1, other_edge.node1, other_edge.node2) != Edge.ccw(self.node2, other_edge.node1, other_edge.node2) and \
			Edge.ccw(self.node1, self.node2, other_edge.node1) != Edge.ccw(self.node1, self.node2, other_edge.node2)

		return does_intersect

	def __str__(self):
		return str((self.node1, self.node2))

	def __repr__(self):
		return self.__str__()