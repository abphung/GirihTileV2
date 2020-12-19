from Edge import Edge
from Node import Node
from typing import List
from random import choice

class Polygon:

	edges: list
	open_edges: list
	removed_open_edge = {}

	@staticmethod
	def create(PolygonType, node_set, edge_set):
		init_edge = Edge(Node(0, 0), Node(0, node_set.scale))
		init_edge.reverse()
		_, valid_new_edges = Polygon.place(PolygonType, init_edge, 0, node_set, edge_set)
		return PolygonType([], valid_new_edges, node_set, edge_set)

	def __init__(self, joining_edges: List['Edge'], valid_edges: List['Edge'], node_set: 'NodeSet', edge_set: 'EdgeSet'):
		self.edges = valid_edges
		self.open_edges = []
		for edge in valid_edges:
			if edge in joining_edges:
				if edge in edge.polygon1.open_edges:
					edge.close()
					edge.polygon1.open_edges.remove(edge)
					Polygon.removed_open_edge[edge] = (type(edge.polygon1), type(self))
				else:
					print("trying to removing an edge not in open edges!", edge, edge.polygon1.open_edges)
					if edge in Polygon.removed_open_edge.keys():
						print("was previously removed", Polygon.removed_open_edge[edge])
				edge.polygon1, edge.polygon2 = self, edge.polygon1
			else:
				node_set.add(edge.node1)
				edge_set.add(edge)
				edge.polygon1 = self
				self.open_edges.append(edge)		

	def get_open_edge(self):
		return choice(self.open_edges)

	@staticmethod
	def place(PolygonType, starting_edge, start_index, node_set, edge_set):
		angles_len = len(PolygonType.angles)
		starting_edge.reverse()
		past_edge = starting_edge
		if not starting_edge.open:
			print("Starting edge is not open!!")
			return (None, None)
		joining_edges = []
		valid_edges = []
		for i in range(angles_len):
			angle_abs_value = PolygonType.angles[(start_index + i)%angles_len]
			new_relative_angle = past_edge.offset_relative_angle_clockwise(angle_abs_value)
			new_node1 = past_edge.node2

			#validate
			edge_angle_intersects, node_resultant_angle_too_small, edge_intersects = False, False, False

			#check valid node. if new node it is always valid
			is_new_node, new_node2 = Node.create(new_relative_angle, new_node1, node_set)
			if not is_new_node:
				edge_angle_intersects = new_node1.intersects(new_relative_angle)
				node_resultant_angle_too_small = new_node1.invalid_resultant_angle(angle_abs_value)

			#check valid edge. If it is an existing edge it is always valid
			is_new_edge, new_edge = Edge.create(new_node1, new_node2, edge_set)
			if not is_new_edge:
				joining_edges.append(new_edge)
			else:
				edge_intersects = edge_set.intersects(new_edge)
			
			if edge_intersects or edge_angle_intersects or node_resultant_angle_too_small:

				for joining_edge in joining_edges:
					joining_edge.reverse()
				if not starting_edge in joining_edges:
					starting_edge.reverse()
				return (None, None)
				
			new_node1.closed_angles.append((past_edge.relative_angle(), new_relative_angle))
			valid_edges.append(new_edge)
			past_edge = new_edge

		return (joining_edges, valid_edges)

	def clockwise_nodes(self) -> List['Node']:
		nodes = []
		for edge in self.edges:
			if edge.polygon1 == self:
				nodes.append(edge.node1)
			else:
				nodes.append(edge.node2)
		return nodes

	def __str__(self):
		return str(self.edges)

	def __repr__(self):
		return self.__str__()

	