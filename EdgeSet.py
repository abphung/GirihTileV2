from math import floor, ceil

class EdgeSet:

	def __init__(self, width: int, height: int, node_set: 'NodeSet'):
		self.width = width
		self.height = height
		self.scale = node_set.scale
		x_width = ceil(width/self.scale)
		y_height = ceil(height/self.scale)
		self.edges = [[[] for x in range(x_width)] for y in range(y_height)]

	def neighbors(self, node: 'Node'):
		x, y = self.resize(node.x), self.resize(node.y)
		locations = [(x, y)]
		if x > 0:
			locations.append((x - 1, y))
		if x < self.width - 1:
			locations.append((x + 1, y))
		if x > 0:
			locations.append((x, y - 1))
		if x < self.height - 1:
			locations.append((x, y + 1))
		return locations

	def intersects(self, edge: 'Edge'):
		seen_locations = set()
		for location in self.neighbors(edge.node1) + self.neighbors(edge.node2):
			if location not in seen_locations:
				x, y = location
				for other_edges in self.edges[x][y]:
					if edge.intersects(other_edges):
						return True

		return False

	def resize(self, value: int) -> int:
		return floor(value/self.scale)

	def try_get(self, node1: 'Node', node2: 'Node'):
		resized_1_x = self.resize(node1.x)
		resized_1_y = self.resize(node1.y)
		resized_2_x = self.resize(node2.x)
		resized_2_y = self.resize(node2.y) 
		existing_edges = self.edges[resized_1_x][resized_1_y]
		existing_edges += self.edges[resized_2_x][resized_2_y]
		for existing_edge in existing_edges:
			if node2 == existing_edge.node1 and node1 == existing_edge.node2:
				existing_edge.reverse()
				return existing_edge
			elif node2 == existing_edge.node2 and node1 == existing_edge.node1:
				return existing_edge

	def add(self, edge: 'Edge'):
		resized_1_x = self.resize(edge.node1.x)
		resized_1_y = self.resize(edge.node1.y)
		resized_2_x = self.resize(edge.node2.x)
		resized_2_y = self.resize(edge.node2.y) 
		self.edges[resized_1_x][resized_1_y].append(edge)
		if resized_1_x != resized_2_x or resized_1_y != resized_2_y:
			self.edges[resized_1_y][resized_2_y].append(edge)