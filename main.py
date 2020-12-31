from TilingEngine import TilingEngine
from RenderingEngineMatplotlib import RenderingEngineMatplotlib
from PolygonTypes import *

if __name__ == "__main__":
	polygons = TilingEngine.tile(1000, [Bowtie, Decagon, Hexagon, Pentagon, Rhombus])
	renderingEngine = RenderingEngineMatplotlib(2000, 2000)
	renderingEngine.draw(polygons)