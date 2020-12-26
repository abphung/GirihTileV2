import matplotlib.pyplot as plt
from random import choice 

class RenderingEngineMatplotlib:

	def __init__(self, width = 800, height = 800):
		self.width = width
		self.height = height
		self.x_offset = width/2
		self.y_offset = height/2

	def draw(self, polygons):
		my_dpi=96
		plt.figure(figsize=(self.width/my_dpi, self.height/my_dpi), dpi=my_dpi)
		plt.xlim([0, self.width])
		plt.ylim([0, self.height])
		for polygon in polygons:
			points = list(map(lambda node: node.pair(self.x_offset, self.y_offset), polygon.ordered_nodes))
			color = (choice(range(255)), choice(range(255)), choice(range(255)))
			x, y = map(list, zip(*points))
			plt.fill(x, y, color)
		plt.show()