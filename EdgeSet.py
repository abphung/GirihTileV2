from math import floor, ceil

class EdgeSet:

	def __init__(self, width: int, height: int, node_set: 'NodeSet'):
		self.width = width
		self.height = height
		self.scale = node_set.scale
		self.edges = {}

	def neighbors(self, node: 'Node'):
		x, y = self.get_coords(node)
		locations = [(x, y)]
		locations.append((x - 1, y))
		locations.append((x + 1, y))
		locations.append((x, y - 1))
		locations.append((x, y + 1))
		return locations

	def intersects(self, edge: 'Edge'):
		for coords in set(self.neighbors(edge.node1) + self.neighbors(edge.node2)):
			if coords in self.edges.keys():
				for other_edge in self.edges[coords]:
					if edge is not other_edge and edge.intersects(other_edge):
						return True
		return False

	def get_coords(self, node: 'Node') -> (int, int):
		return (floor(node.x/self.scale), floor(node.y/self.scale))

	def try_get(self, node1: 'Node', node2: 'Node'):
		node1_coords = self.get_coords(node1)
		if node1_coords not in self.edges.keys():
			return None
		node2_coords = self.get_coords(node2)
		if node2_coords not in self.edges.keys():
			return None
		existing_edges = self.edges[node1_coords] + self.edges[node2_coords]
		for existing_edge in existing_edges:
			if node2 == existing_edge.node1 and node1 == existing_edge.node2 or\
				node2 == existing_edge.node2 and node1 == existing_edge.node1:
				return existing_edge

	def try_add(self, edge: 'Edge'):
		node1_coords = self.get_coords(edge.node1)
		if node1_coords not in self.edges.keys():
			self.edges[node1_coords] = []
		node2_coords = self.get_coords(edge.node2)
		if node2_coords not in self.edges.keys():
			self.edges[node2_coords] = []
		should_add = edge not in self.edges[self.get_coords(edge.node1)]
		if should_add:
			self.edges[node1_coords].append(edge)
			node2_coords = self.get_coords(edge.node2)
			if self.get_coords(edge.node1) != node2_coords and \
				edge not in self.edges[self.get_coords(edge.node2)]:
				self.edges[node2_coords].append(edge)
		return should_add

	def try_remove(self, edge: 'Edge'):
		removed = False
		node1_coords = self.get_coords(edge.node1)
		if node1_coords in self.edges.keys() and edge in self.edges[node1_coords]:
			self.edges[node1_coords].remove(edge)
			removed = True
		node2_coords = self.get_coords(edge.node2)
		if node2_coords in self.edges.keys() and edge in self.edges[node2_coords]:
			self.edges[node2_coords].remove(edge)
			removed = True
		return removed