from TilingEngine import TilingEngine
from RenderingEngineMatplotlib import RenderingEngineMatplotlib

if __name__ == "__main__":
	polygons = TilingEngine.tile(10)
	renderingEngine = RenderingEngineMatplotlib(2000, 2000)
	renderingEngine.draw(polygons)