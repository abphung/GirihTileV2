from math import cos, sin, radians

class Node:

	@staticmethod
	def create(angle: int, relative_to_node: 'Node', node_set: 'NodeSet') -> 'Node':
		x = round(relative_to_node.x + node_set.scale*cos(radians(angle)))
		y = round(relative_to_node.y + node_set.scale*sin(radians(angle)))
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
		return obj != None and self.x == obj.x and self.y == obj.y

	def __hash__(self):
		return hash((self.x, self.y))

	def intersects(self, relative_angle: int) -> bool:
		for start_rel_angle, end_rel_angle in self.closed_angles:
			if start_rel_angle < end_rel_angle:
				return start_rel_angle < relative_angle < end_rel_angle
			elif start_rel_angle > end_rel_angle:
				return relative_angle > start_rel_angle or relative_angle < end_rel_angle
			else:
				return False

	def min_gap(self, start, end):
		sorted_angles = sorted(self.closed_angles + [(start, end)], key=lambda this_range: this_range[0])
		length = len(sorted_angles)
		#subtract 1 so non gaps(which will have size 0) will not be considered in the min
		return min([(sorted_angles[(i + 1)%length][0] - sorted_angles[i][1] - 1)%360 + 1 for i in range(length)])

	def pair(self, x_off, y_off):
		return (self.x + x_off, y_off - self.y)