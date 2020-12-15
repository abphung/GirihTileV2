from random import *
import unittest
from math import *
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import sys

class Node:
	x: int 
	y: int
	closed_angles: list
	x_offset = 400
	y_offset = 300
	scale = 100
	instances = []

	def init(angle, relative_to_node):
		x = relative_to_node.x + Node.scale*cos(radians(angle))
		y = relative_to_node.y + Node.scale*sin(radians(angle))
		for existing_node in Node.instances:
			if round(x) == round(existing_node.x) and round(y) == round(existing_node.y):
				return (False, existing_node)
		new_node = Node(x, y)
		return (True, new_node)

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.closed_angles = []

	def valid(node, relative_angle, total_angle):
		for closed_angle in node.closed_angles:
			if closed_angle[0] < relative_angle < closed_angle[1] or closed_angle[0] < relative_angle - 360 < closed_angle[1]:
				# print(closed_angle[0], relative_angle, closed_angle[1])
				return False
		if 0 < 360 - sum(map(lambda x: x[1] - x[0], node.closed_angles)) - total_angle < 72:
			# print(node.closed_angles)
			# print(360 - sum(map(lambda x: x[1] - x[0], node.closed_angles)) - total_angle)
			return False

		return True

	def pair(self):
		return (round(self.x) + Node.x_offset, round(self.y) + Node.y_offset)

	def __str__(self):
		return str(self.pair())

	def __repr__(self):
		return self.__str__()

	def __eq__(self, obj):
		return round(self.x) == round(obj.x) and round(self.y) == round(obj.y)

class Polygon:

	edges: list
	open_edges: list
	removed_open_edge = {}

	def init(PolygonType):
		init_edge = Edge(Node(0, 0), Node(0, Node.scale))
		init_edge.reverse()
		_, valid_new_edges = Polygon.valid(PolygonType, init_edge, 0)
		return PolygonType([], valid_new_edges)

	def __init__(self, joining_edges, valid_edges):
		self.edges = valid_edges
		self.open_edges = []
		for edge in valid_edges:
			if edge in joining_edges:
				if edge in edge.polygon1.open_edges:
					edge.close()
					edge.polygon1.open_edges.remove(edge)
					Polygon.removed_open_edge[edge] = (type(edge.polygon1), type(self))
				else:
					Drawer.highlights.append((edge, "red"))
					print("trying to removing an edge not in open edges!", edge, edge.polygon1.open_edges)
					if edge in Polygon.removed_open_edge.keys():
						print("was previously removed", Polygon.removed_open_edge[edge])
				edge.polygon1, edge.polygon2 = self, edge.polygon1
			else:
				edge.exists()
				edge.polygon1 = self
				self.open_edges.append(edge)		

	def get_open_edge(self):
		return choice(self.open_edges)

	#only need open edges not global edges
	def valid(PolygonType, starting_edge, start_index):
		angles_len = len(PolygonType.angles)
		starting_edge.reverse()
		past_edge = starting_edge
		if not starting_edge.open:
			Drawer.highlights.append((starting_edge, "red"))
			print("Starting edge is not open!!")
			return (None, None)
		joining_edges = []
		valid_edges = []
		#Drawer.highlights.append((starting_edge, "green"))
		for i in range(angles_len):
			new_angle = (past_edge.angle() + 180)%360 - PolygonType.angles[(start_index + i)%angles_len]
			new_node1 = past_edge.node2
			is_new_node, new_node2 = Node.init(new_angle, new_node1)
			is_new_edge, new_edge = Edge.init(new_node1, new_node2)
			if not is_new_edge:
				joining_edges.append(new_edge)
			if any(map(new_edge.intersects, Edge.instances)) or not Node.valid(new_node1, new_angle, PolygonType.angles[(start_index + i)%angles_len]):
				# print("failed to connect ", PolygonType)
				for joining_edge in joining_edges:
					joining_edge.reverse()
					# print("is reversed, joining edge, starting edge: ", joining_edge.reversed, joining_edge, starting_edge)
				if not starting_edge in joining_edges:
					starting_edge.reverse()
				return (None, None)
			else:
				#print(PolygonType,(cur_edge.angle() + 180)%360, new_angle)
				new_node1.closed_angles.append((new_angle, (past_edge.angle() + 180)%360))
			valid_edges.append(new_edge)
			past_edge = new_edge

		#walk along generating nodes and adding edges theoretically.
		#if everything looks good then actually init else dispose of nodes and edges and try another polygon
		#print(joining_edges, new_edges)
		#Drawer.highlights.append((past_edge, "blue"))
		return (joining_edges, valid_edges)

	def __str__(self):
		return str(self.edges)

	def __repr__(self):
		return self.__str__()

class Edge:
	node1: Node
	node2: Node
	polygon1: Polygon
	polygon2: Polygon
	instances = []

	def init(node1, node2):
		for existing_edge in Edge.instances:
			if node2 == existing_edge.node1 and node1 == existing_edge.node2:
				existing_edge.reverse()
				return (False, existing_edge)
			elif node2 == existing_edge.node2 and node1 == existing_edge.node1:
				return (False, existing_edge)
		new_edge = Edge(node1, node2)
		return (True, new_edge)

	def __init__(self, node1, node2):
		self.node1 = node1
		self.node2 = node2
		self.reversed = False
		self.open = True

	# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
	def ccw(A,B,C):
		return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

	def intersects(self, other_edge):
		if self is other_edge or sum([self.node1 == other_edge.node2, self.node2 == other_edge.node1, self.node1 == other_edge.node1, self.node2 == other_edge.node2]) == 1:
			return False
		does_intersect = Edge.ccw(self.node1, other_edge.node1, other_edge.node2) != Edge.ccw(self.node2, other_edge.node1, other_edge.node2) and \
			Edge.ccw(self.node1, self.node2, other_edge.node1) != Edge.ccw(self.node1, self.node2, other_edge.node2)
		# if does_intersect:
		# 	print(self, other_edge)
		return does_intersect

	#returns int in range [0, 360]
	def angle(self):
		# instead of doing node1 - node2 do node2 - node1 + 180 so all angles are positive
		return round(degrees(atan2(self.node1.y - self.node2.y, self.node1.x - self.node2.x)) + 180)

	def reverse(self):
		self.reversed = not self.reversed
		self.node1, self.node2 = self.node2, self.node1

	def exists(self):
		if self not in Edge.instances:
			Edge.instances.append(self)
		if self.node1 not in Node.instances:
			Node.instances.append(self.node1)
		if self.node2 not in Node.instances:
			Node.instances.append(self.node2)

	def close(self):
		self.open = False

	def __str__(self):
		return str((self.node1, self.node2))

	def __repr__(self):
		return self.__str__()

class Bowtie(Polygon):
	angles = [72, 72, 216, 72, 72, 216]

class Decagon(Polygon):
	angles = [144]*10

class Hexagon(Polygon):
	angles = [72, 144, 144, 72, 144, 144]

class Pentagon(Polygon):
	angles = [108]*5

class Rhombus(Polygon):
	angles = [72, 108, 72, 108]

class Drawer:
	highlights = []

	def __init__(self, width = 800, height = 800):
		self.width = width
		self.height = height
		Node.x_offset = width/2
		Node.y_offset = height/2
		self.image = Image.new("RGB", (self.width, self.height))
		self.image_draw = ImageDraw.Draw(self.image)

	def draw(self, polygons):	
		for polygon in polygons:
			points = list(map(lambda edge: edge.node2.pair() if edge.polygon1 is polygon else edge.node1.pair(), polygon.edges))
			color = (choice(range(255)), choice(range(255)), choice(range(255)))
			self.image_draw.polygon((points), fill=color)
		for edge in Drawer.highlights:
			if type(edge) is tuple:
				edge, color = edge
			else:
				color = "red"
			self.image_draw.line((edge.node1.pair(), edge.node2.pair()), fill=color, width = 5)
		self.image.show()

class UnitTests(unittest.TestCase):

	def test_hexagon(self):
		polygons = self.perform_test_n([Hexagon], [], [6], True, False)

	def test_hexagon_hexagon(self):
		self.perform_test_n([Hexagon, Hexagon], [(0, 0, 0)], [len(Hexagon.angles) - 1, len(Hexagon.angles) - 1], True, False)

	def test_bowtie_decagon(self):
		self.perform_test(Bowtie, Decagon, True, False, 1, 0, )

		self.perform_test_n([Bowtie, Decagon], [(0, 1, 0)], [len(Bowtie.angles) - 2, len(Decagon.angles) - 2], True, False)

	def test_bowtie_hexagon(self):
		self.perform_test(Bowtie, Hexagon, True, False, 1, 0, len(Bowtie.angles) - 2, len(Hexagon.angles) - 2)

	def test_hexagon_bowtie(self):
		self.perform_test(Hexagon, Bowtie, True, False, 0, 0, len(Hexagon.angles) - 2, len(Bowtie.angles) - 2)

	def test_pentagon_bowtie(self):
		self.perform_test(Pentagon, Bowtie, False, False, 0, 0, None, None)

	def test_bowtie_bowtie(self):
		self.perform_test(Bowtie, Bowtie, False, False, 1, 0, None, None)

	def test_bowtie_hexagon_pentagon(self):
		self.perform_test_n([Bowtie, Hexagon, Pentagon], [(0, 2, 0), (1, 4, 0)], None, False, False)

	def test_decagon_bowtie(self):
		self.perform_test_n([Decagon, Bowtie], [(0, 5, 0)], [8, 4], True, False)

	def test_decagon_hexagon_hexagon_bowtie(self):
		self.perform_test_n([Decagon, Hexagon, Hexagon, Bowtie], [(0, 0, 0), (0, 2, 1), (0, 1, 1)], [7, 3, 3, 1], True, False)

	def test_pentagon_hexagon_decagon(self):
		self.perform_test_n([Pentagon, Hexagon, Decagon], [(0, 0, 0), (1, 4, 0)], None, False, False)

	def test_pentagron_rhombus_pentagon_decagon_bowtie(self):
		self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (2, 0, 1)], [], False, False)
		self.perform_test_n([Pentagon, Rhombus, Pentagon, Decagon, Bowtie], [(0, 2, 1), (0, 3, 0), (0, 1, 0), (1, 2, 2)], [], False, False)

	def test_decagon_decagon_decagon(self):
		self.perform_test_n([Decagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False, False)

	def test_pentagon_decagon_decagon(self):
		self.perform_test_n([Pentagon, Decagon, Decagon], [(0, 0, 0), (0, 1, 0)], [], False, False)

	def test_decagon_bowtie_pentagon(self):
		self.perform_test_n([Decagon, Bowtie, Pentagon], [(0, 0, 0), (0, 2, 0)], [], False, False)

	def test_bowtie_bowtie_bowtie(self):
		self.perform_test_n([Decagon, Bowtie, Pentagon], [(0, 0, 0), (0, 2, 0)], [], False, False)

	#random placement tests
	def test_bowtie_bowtie_bowtie_placement(self):
		pass
	
	def perform_test(self, Polygon1, Polygon2, valid, should_draw, polygon1_join_side, polygon2_join_side, polygon1_open_count, polygon2_open_count):
		Node.instances = []
		Edge.instances = []
		Drawer.highlights = []
		polygon1 = Polygon.init(Polygon1)
		joining_edges, valid_new_edges = Polygon.valid(Polygon2, polygon1.edges[polygon1_join_side], start_index = polygon2_join_side)
		if valid_new_edges != None:
			polygon2 = Polygon2(joining_edges, valid_new_edges)
			if should_draw:
				Drawer().draw([polygon1, polygon2])

		if valid:
			self.assertTrue(valid_new_edges != None)
			self.assertTrue(polygon1 != None)
			self.assertTrue(polygon2 != None)
			self.assertEqual(len(polygon1.open_edges), polygon1_open_count)
			self.assertEqual(len(polygon2.open_edges), polygon2_open_count)
		else:
			self.assertTrue(valid_new_edges == None)

	def perform_test_n(self, polygon_types, joining_edges_collection, polygons_open_count, valid, should_draw):
		Node.instances = []
		Edge.instances = []
		Drawer.highlights = []
		polygons = [Polygon.init(polygon_types[0])]
		is_invalid_edge_present = False
		for PolygonType in polygon_types[1:]:
			polygon1_index, polygon1_side_index, polygon2_side_index = joining_edges_collection.pop(0)
			joining_edges, valid_new_edges = Polygon.valid(PolygonType, polygons[polygon1_index].edges[polygon1_side_index], start_index = polygon2_side_index)
			if valid_new_edges == None:
				is_invalid_edge_present = True
				break
			polygons.append(PolygonType(joining_edges, valid_new_edges))

		if should_draw:
			Drawer().draw(polygons)

		if valid:
			self.assertEqual(len(polygons), len(polygon_types))
			for i, open_count in enumerate(polygons_open_count):
				self.assertEqual(len(polygons[i].open_edges), open_count)
		else:
			self.assertTrue(is_invalid_edge_present)

		return polygons

	def perform_random_placement_test

if __name__ == "__main__":
	run_unit_tests = False
	if run_unit_tests:
		unittest.main()
	else:
		#compute 
		drawer = Drawer()
		polygon_types = [Bowtie, Decagon, Hexagon, Pentagon, Rhombus]
		polygons = []

		InitPolygonType = choice(polygon_types)
		init_polygon = Polygon.init(InitPolygonType)
		polygons.append(init_polygon)
		open_polygons = [init_polygon]
		for i in range(2):
			cur_polygon = open_polygons.pop(0)
			while cur_polygon.open_edges == []:
				cur_polygon = open_polygons.pop(0)
			while cur_polygon.open_edges != []:
				cur_edge = cur_polygon.get_open_edge()
				possibilities = [(PolygonType, i) for PolygonType in polygon_types for i in range(len(PolygonType.angles))]
				shuffle(possibilities)
				found_valid_polygon = False
				for possibility in possibilities:
					NewPolygonType, start_index = possibility
					joining_edges, valid_new_edges = Polygon.valid(NewPolygonType, cur_edge, start_index)
					if valid_new_edges != None:
						new_polygon = NewPolygonType(joining_edges, valid_new_edges)
						polygons.append(new_polygon)
						open_polygons.append(new_polygon)
						found_valid_polygon = True
						break
				if not found_valid_polygon:
					cur_polygon.open_edges.remove(cur_edge)
					Drawer.highlights.append((cur_edge, "white"))

			if cur_polygon.open_edges != []:
				open_polygons.append(cur_polygon)
		print(list(map(type, polygons)))
		for edge in Edge.instances:
			if edge.open:
				Drawer.highlights.append((edge, "blue"))
		drawer.draw(polygons)
		