import matplotlib.pyplot as plt
from random import choice 

class RenderingEngineMatplotlib:

	def __init__(self, width = 800, height = 800):
		self.width = width
		self.height = height

	def draw(self, polygons):
		my_dpi=96
		plt.figure(figsize=(self.width/my_dpi, self.height/my_dpi), dpi=my_dpi)
		plt.xlim([-self.width/2, self.width/2])
		plt.ylim([-self.height/2, self.height/2])
		for polygon in polygons:
			points = list(map(lambda node: node.pair(0, 0), polygon.ordered_nodes))
			color = (choice(range(255)), choice(range(255)), choice(range(255)))
			x, y = map(list, zip(*points))
			plt.fill(x, y, color)
		plt.show()