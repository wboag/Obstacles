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
from empiricalMDP import EmpiricalMDP
from valueIterationAgent import ValueIterationAgent



def flipCoin( p ):
    r = random.random()
    return r < p


class agent(object):

	def __init__(self):
		self.rewardValues = { 'mountain':3, 'forest':4, 'water':4, 'grass':5 }
		self.skillLevels  = { 'mountain':1, 'forest':1, 'water':1, 'grass':1 }
		self.index = None

	def getSkill(self, skill):
		return self.skillLevels[skill]

	def getWaterSkill(self):
		return self.getSkill('water')

	def getGrassSkill(self):
		return self.getSkill('grass')

	def getForestSkill(self):
		return self.getSkill('forest')

	def getMountainSkill(self):
		return self.getSkill('mountain')

	def setSkill(self, skill, val):
		self.skillLevels[skill] = val

	def setWaterSkill(self, val):
		self.setSkill('water', val)

	def setGrassSkill(self, val):
		self.setSkill('grass', val)

	def setForestSkill(self, val):
		self.setSkill('forest', val)

	def setMountainSkill(self, val):
		self.setSkill('mountain', val)

	def __eq__(self, arg):
		return arg.type == self.type and arg.index == self.index

	def getIndex(self):
		return self.index

	def setIndex(self, value):
		self.index = value

	
class randomAgent(agent):
	
	def __init__(self):
		super(randomAgent, self).__init__()
		self.type = "random"

	def chooseAction(self, actions):
		filteredActions = filter(lambda n: n == 'east' or n == 'north' or n == 'finish', actions)
		return random.choice(filteredActions)
	
	def update(self):
		pass

class adpAgent(agent):
	
	def __init__(self, gameworld, all_qstate_results):
		super(adpAgent, self).__init__()
		self.type = "adp"

		# Parameters
		self.epsilon = 0.0

		for it in all_qstate_results:
			print it
		#exit()

		# Estimate of model
		self.empirical_mdp = EmpiricalMDP(all_qstate_results, self.skillLevels)
		self.solver = ValueIterationAgent(self.empirical_mdp, iterations=100)

		print 'boop'
		#exit()

	def setEpsilon(self, epsilon):
		self.epsilon = epsilon


	def update(self, state, terrain, action, nextState, reward):
		"""
		print 'oldState: ', oldState
		print 'terrainType: ', terrainType
		print 'action: ', action
		print 'newState: ', newState
		print 'reward: ', reward
		print
        """
		self.empirical_mdp.updateTransition(state, action, nextState, reward, terrain)


	def chooseAction(self, actions, state, terrainType):
		###Your Code Here :)###
		if flipCoin(self.epsilon):
			return random.choice(self.empirical_mdp.getPossibleActions(state))
		else:
			return self.solver.computeActionFromValues(state)


class tdAgent(agent):
	
	def __init__(self, goalPosition):
		super(tdAgent, self).__init__()
		self.type = "td"
		self.goalPosition = goalPosition
		###Your Code Here :)###

	def update(self, oldState, terrainType, action, newState, reward):
		###Your Code Here :)###
		pass

	def chooseAction(self, actions, state, terrainType):
		###Your Code Here :)###
		filteredActions = filter(lambda n: n == 'east' or n == 'north' or n == 'finish', actions)
		return random.choice(filteredActions)  
