####
#
# Agents
# Jake Kinsman
# 11/28/2014
#
####

###
# README:
#
# 1.  If you want a dictionary with a default value (util.counters from UC Berkeley Problem Sets), 
#       use a defaultdict as shown:  a = defaultdict(lambda: <DEFAULT-VALUE> )
#
# 2.  Choose action should use your current model of the world (however you choose to store it), 
#       and compute the optimal action to be taken.  If you are in a terminal state, the only action is "finish"
#
# 3.  Update needs to perform whatever learning is needed to your model after each action is performed.
#
# 4.  the gameworld variable passed to your agents methods should contain all information required to perform your computations.
#
# 5.  Feel free to add more methods as needed!  training the agents only calls the methods provided, 
#       and racing only calls chooseAction()
###

###
# GAMEWORLD FUNCTIONALITY:
# def getDiscount(self):
#   returns discount factor [0,1)
# def getLivingReward(self):
#    returns reward for staying alive
# 
###


import random
from collections import defaultdict

class agent(object):
	
	def __init__(self):
		self.waterSkill = 1
		self.grassSkill = 1
		self.mountainSkill = 1
		self.forestSkill = 1
		self.index = None

	def __eq__(self, arg):
		return arg.type == self.type and arg.index == self.index

	def setWaterSkill(self, value):
		self.waterSkill = value
	
	def setGrassSkill(self, value):
		self.grassSkill = value
	
	def setMountainSkill(self, value):
		self.mountainSkill = value
	
	def setForestSkill(self, value):
		self.forestSkill = value
	
	def setIndex(self, value):
		self.index = value

	def getWaterSkill(self):
		return self.waterSkill
	
	def getGrassSkill(self):
		return self.grassSkill
	
	def getMountainSkill(self):
		return self.mountainSkill
	
	def getForestSkill(self):
		return self.forestSkill
	
	def getIndex(self):
		return self.index
	
class randomAgent(agent):
	
	def __init__(self):
		super(randomAgent, self).__init__()
		self.type = "random"

	def chooseAction(self, gameworld):
		actions = gameworld.getActions(gameworld.getAgentState(self))
		filteredActions = filter(lambda n: n == 'east' or n == 'north' or n == 'finish', actions)
		return random.choice(filteredActions)
	
	def update(self):
		pass

class adpAgent(agent):
	
	def __init__(self):
		super(adpAgent, self).__init__()
		self.type = "adp"
		###Your Code Here :)###

	def update(self):
		###Your Code Here :)###
		pass

	def chooseAction(self, gameworld):
		###Your Code Here :)###
		actions = gameworld.getActions(gameworld.getAgentState(self))
		filteredActions = filter(lambda n: n == 'east' or n == 'north' or n == 'finish', actions)
		return random.choice(filteredActions)  

class tdAgent(agent):
	
	def __init__(self):
		super(tdAgent, self).__init__()
		self.type = "td"
		###Your Code Here :)###

	def update(self):
		###Your Code Here :)###
		pass

	def chooseAction(self, gameworld):
		###Your Code Here :)###
		actions = gameworld.getActions(gameworld.getAgentState(self))
		filteredActions = filter(lambda n: n == 'east' or n == 'north' or n == 'finish', actions)
		return random.choice(filteredActions)  
