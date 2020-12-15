from Polygon import Polygon

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