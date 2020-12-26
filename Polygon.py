from Edge import Edge
from Node import Node
from typing import List
from random import choice

class Polygon:

	@staticmethod
	def create(PolygonType, node_set, edge_set):
		init_edge = Edge(Node(0, 0), Node(0, node_set.scale))
		valid_new_edges = Polygon.place(PolygonType, init_edge, 0, node_set, edge_set)
		return PolygonType(valid_new_edges, node_set, edge_set)

	def __init__(self, valid_edges: List['Edge'], node_set: 'NodeSet', edge_set: 'EdgeSet'):
		self.edges = valid_edges
		self.ordered_nodes = []
		for edge in valid_edges:
			# if edge in joining_edges:
			# 	if edge in edge.polygon1.open_edges:
			# 		edge.close()
			# 		edge.polygon1.open_edges.remove(edge)
			# 		Polygon.removed_open_edge[edge] = (type(edge.polygon1), type(self))
			# 	else:
			# 		print("trying to removing an edge not in open edges!", edge, edge.polygon1.open_edges)
			# 		if edge in Polygon.removed_open_edge.keys():
			# 			print("was previously removed", Polygon.removed_open_edge[edge])
			# 	edge.polygon1, edge.polygon2 = self, edge.polygon1
			# else:
			node_set.add(edge.node1)
			node_set.add(edge.node2)
			if edge_set.try_add(edge):
				edge_set.open_edges.append(edge)
				self.ordered_nodes.append(edge.node1)
			else:
				edge_set.open_edges.remove(edge)
				self.ordered_nodes.append(edge.node2)

	@staticmethod
	def place(PolygonType, starting_edge, start_index, node_set, edge_set, allow_collisions = False):
		angles_len = len(PolygonType.angles)
		#past_edge = starting_edge
		cur_relative_angle = (starting_edge.relative_angle + 180)%360
		cur_node = starting_edge.node1
		valid_edges = []
		for i in range(angles_len):
			angle_abs_value = PolygonType.angles[(start_index + i)%angles_len]
			new_relative_angle = (cur_relative_angle + 180 + angle_abs_value)%360#cur_edge.offset_relative_angle_clockwise(angle_abs_value)

			#validate
			edge_angle_intersects, node_resultant_angle_too_small, edge_intersects = False, False, False

			#check valid node. if new node it is always valid
			is_new_node, new_node = Node.create(new_relative_angle, cur_node, node_set)
			if not is_new_node:
				edge_angle_intersects = cur_node.intersects(new_relative_angle)
				node_resultant_angle_too_small = 0 < cur_node.min_gap(cur_relative_angle, new_relative_angle) < 72

			#check valid edge. If it is an existing edge it is always valid
			is_new_edge, new_edge = Edge.create(cur_node, new_node, edge_set)
			if is_new_edge:
				edge_intersects = edge_set.intersects(new_edge)

			if not allow_collisions and (edge_intersects or edge_angle_intersects or node_resultant_angle_too_small):
				return None
				
			cur_node.closed_angles.append((cur_relative_angle, new_relative_angle))
			valid_edges.append(new_edge)

			cur_relative_angle = new_relative_angle
			cur_node = new_node

		return valid_edges

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

	