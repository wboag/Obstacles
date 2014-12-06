####
#
# State
# Jake Kinsman
# 11/28/2014
#
####

#file tested

class state(object):
	
	def __init__(self, position = (0, 9), terrainNum = 0):
		self.position = position
		self.world = terrainNum
		self.terrainType = None
	
	def __repr__(self):
		return "Position: " + str(self.position) + " " + "Terrain: " + str(self.world)
	
	def __eq__(self, arg):
		return arg.getPosition() == self.getPosition() and self.getWorld() == arg.getWorld()

	def __hash__(self):
		x,y = self.getPosition()
		w = self.getWorld()
		if x == float('inf'): return 1001
		if y == float('inf'): return 1002
		return 100*w + 10*y + x

	def getState(self):
		return [self.position, self.world]
	
	def setPosition(self, position, terrainNum):
		self.position = position
		self.world = terrainNum
	
	def getPosition(self):
		return self.position

	def getWorld(self):
		return self.world
	
	def setWorld(self, value = 0):
		self.world = value

	def setTerrainType(self, terrainType):
		self.terrainType = terrainType
	
	def getTerrainType(self):
		return self.terrainType