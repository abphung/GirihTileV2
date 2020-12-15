import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
from random import choice 

class RenderingEngine:

	def __init__(self, width = 800, height = 800):
		self.width = width
		self.height = height
		self.x_offset = width/2
		self.y_offset = height/2
		self.image = Image.new("RGB", (self.width, self.height))
		self.image_draw = ImageDraw.Draw(self.image)

	def draw(self, polygons):	
		for polygon in polygons:
			points = list(map(lambda edge: edge.node2.pair(self.x_offset, self.y_offset) if edge.polygon1 is polygon else edge.node1.pair(self.x_offset, self.y_offset), polygon.edges))
			color = (choice(range(255)), choice(range(255)), choice(range(255)))
			self.image_draw.polygon((points), fill=color)
		# for edge in Drawer.highlights:
		# 	if type(edge) is tuple:
		# 		edge, color = edge
		# 	else:
		# 		color = "red"
		# 	self.image_draw.line((edge.node1.pair(self.x_offset, self.y_offset), edge.node2.pair(self.x_offset, self.y_offset)), fill=color, width = 5)
		self.image.show()