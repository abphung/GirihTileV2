

class NodeSet:

	def __init__(self, scale):
		self.locations = set()
		self.nodes = {}
		self.scale = scale

	def try_get(self, x: int, y: int) -> 'Node':
		if (x, y) in self.locations:
			return self.nodes[(x, y)]
		else:
			return None

	def add(self, node: 'Node'):
		self.locations.add((node.x, node.y))
		self.nodes[(node.x, node.y)] = node