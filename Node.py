from math import *

class Node:

	def create(angle: int, relative_to_node: 'Node', node_set: 'NodeSet') -> 'Node':
		x = relative_to_node.x + node_set.scale*cos(radians(angle))
		y = relative_to_node.y + node_set.scale*sin(radians(angle))
		existing_node = node_set.try_get(x, y)
		if existing_node != None:
			return (False, existing_node)
		new_node = Node(x, y)
		return (True, new_node)

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.closed_angles = []

	def __str__(self):
		return str(self.pair(0, 0))

	def __repr__(self):
		return self.__str__()

	def __eq__(self, obj):
		return obj != None and round(self.x) == round(obj.x) and round(self.y) == round(obj.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def intersects(self, relative_angle: int) -> bool:
		for closed_angle in self.closed_angles:
			print(closed_angle, relative_angle)
			if closed_angle[0] < relative_angle < closed_angle[1] or closed_angle[0] < relative_angle - 360 < closed_angle[1]:
				# print(closed_angle[0], relative_angle, closed_angle[1])
				return True

		return False

	def invalid_resultant_angle(self, additional_angle: int) -> bool:
		if 0 < 360 - sum(map(lambda x: x[1] - x[0], self.closed_angles)) - additional_angle < 72:
			return True

		return False

	def pair(self, x_off, y_off):
		return (self.x + x_off, self.y + y_off)