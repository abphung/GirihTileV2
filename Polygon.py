from Edge import Edge
from Node import Node
from typing import List
from random import choice

class Polygon:

	@staticmethod
	def create(PolygonType, polygon_set: 'PolygonSet'):
		init_edge = Edge(Node(0, 0), Node(0, polygon_set.node_set.scale))
		valid_new_edges = Polygon.place(PolygonType, init_edge, 0, polygon_set)
		return PolygonType(valid_new_edges, polygon_set)

	def __init__(self, valid_edges: List['Edge'], polygon_set: 'PolygonSet'):
		node_set = polygon_set.node_set
		edge_set = polygon_set.edge_set

		self.edges = valid_edges
		self.ordered_nodes = []
		for edge in valid_edges:
			node_set.add(edge.node1)
			node_set.add(edge.node2)
			if edge in polygon_set.open_edges:
				polygon_set.hide(edge)
				self.ordered_nodes.append(edge.node2)
			else:
				edge_set.try_add(edge)
				polygon_set.open_edges[edge] = self
				self.ordered_nodes.append(edge.node1)

	@staticmethod
	def place(PolygonType, starting_edge, start_index, polygon_set: 'PolygonSet', allow_collisions = False):
		node_set = polygon_set.node_set
		edge_set = polygon_set.edge_set
		angles_len = len(PolygonType.angles)
		cur_relative_angle = starting_edge.relative_angle
		cur_node = starting_edge.node1
		valid_edges = []
		reverse_on_failure = []
		for i in range(angles_len):
			angle_abs_value = PolygonType.angles[(start_index + i)%angles_len]
			#adding 180 to flip angle. cur_relative_angle is relative to previous starting node
			new_relative_angle = (cur_relative_angle + 180 + angle_abs_value)%360
			angle_range = ((cur_relative_angle + 180)%360, new_relative_angle)
			#validate
			edge_angle_intersects, node_resultant_angle_too_small, edge_intersects, edge_is_not_open = False, False, False, False

			#check valid node. if new node it is always valid
			_, new_node = Node.create(new_relative_angle, cur_node, node_set)
			if node_set.try_get(cur_node.x, cur_node.y):
				edge_angle_intersects = cur_node.intersects(new_relative_angle)
				node_resultant_angle_too_small = 0 < cur_node.min_gap(*angle_range) < polygon_set.min_angle

			#check valid edge. If it is an existing edge it is always valid
			is_new_edge, new_edge = Edge.create(cur_node, new_node, edge_set)
			if is_new_edge:
				edge_intersects = edge_set.intersects(new_edge)
			else:
				edge_is_not_open = new_edge not in polygon_set.open_edges

			if edge_intersects or edge_angle_intersects or node_resultant_angle_too_small or edge_is_not_open:
				#do not combine condition check with line above so we can set breakpoint in here
				if not allow_collisions:
					for operation, argument in reverse_on_failure:
						operation(argument)
					return None

			cur_node.closed_angles.append(angle_range)
			reverse_on_failure.append((cur_node.closed_angles.remove, angle_range))
			
			valid_edges.append(new_edge)

			cur_relative_angle = new_relative_angle
			cur_node = new_node

		return valid_edges

	def __str__(self):
		return str(self.edges)

	def __repr__(self):
		return self.__str__()