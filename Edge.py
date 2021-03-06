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
		self.reverse_relative_angle = round(degrees(atan2(self.node1.y - self.node2.y, self.node1.x - self.node2.x)) + 180)%360

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

	#this will try to remove angle twice. we only need to remove one node per edge??
	def try_remove_nodes(self, angles_to_remove) -> 'Node':
		removed_node = None
		if self.node1 in angles_to_remove.keys():
			if (self.relative_angle, angles_to_remove[self.node1]) in self.node1.closed_angles:
				self.node1.closed_angles.remove((self.relative_angle, angles_to_remove[self.node1]))
			else:
				print("node1", (self.relative_angle, angles_to_remove[self.node1]), self.node1.closed_angles)
		else:
			angles_to_remove[self.node1] = self.relative_angle
		reversed_angle = (self.relative_angle + 180)%360
		if self.node2 in angles_to_remove.keys():
			if (angles_to_remove[self.node2], reversed_angle) in self.node2.closed_angles:
				self.node2.closed_angles.remove((angles_to_remove[self.node2], reversed_angle))
			else:
				print("node2", (reversed_angle, angles_to_remove[self.node2]), self.node2.closed_angles)
		else:
			angles_to_remove[self.node2] = reversed_angle

	def __str__(self):
		return str((self.node1, self.node2))

	def __repr__(self):
		return self.__str__()