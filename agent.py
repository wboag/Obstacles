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
from  valueIterationAgent import ValueIterationAgent
from policyIterationAgent import PolicyIterationAgent



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

        def endTraining(self):
            self.epsilon = 0.
            self.alpha = 1.
            self.discount = 1.

	
class randomAgent(agent):
	
    def __init__(self):
        super(randomAgent, self).__init__()
        self.type = "random"

    def chooseAction(self, actions):
        if flipCoin(0.08):
            filteredActions = filter(lambda n: n == 'south' or n == 'west' or n == 'finish', actions)
            if filteredActions == []: filteredActions = actions
        else:
            filteredActions = filter(lambda n: n == 'north' or n == 'east' or n == 'finish', actions)
        return random.choice(filteredActions)
	
    def update(self):
        pass


class adpAgent(agent):
	
    def __init__(self, gameworld, all_qstate_results):
        super(adpAgent, self).__init__()
        self.type = "adp"

        # Parameters
        self.epsilon = 0.2

        #return

        # Estimate of model
        self.inferredSkills = { k:1 for k  in ['water','grass','forest','mountain'] }
        self.empirical_mdp = EmpiricalMDP(all_qstate_results, self.rewardValues, self.inferredSkills)
        self.solver = PolicyIterationAgent(self.empirical_mdp, iterations=100)

        #exit()

        # Keep track of number of completed episodes
        self.converged = False
        self.completed = 0
        self.nextUpdate = 1


    def setEpsilon(self, epsilon):
        self.epsilon = epsilon


    def update(self, state, terrain, action, nextState, reward):
        #print 'state:     ', state
        #print 'action:    ', action
        #print 'nextState: ', nextState
        #print 'reward:    ', reward

        # If already converged, then skip update
        if self.converged:
            return

        # update empirical MDP
        self.empirical_mdp.update(state, action, nextState, reward, terrain)

        # If converged AFTER most recent update, then solve MDP for final time
        if self.empirical_mdp.converged():
            #print str(self.completed) + ': final solving'
            self.solver = self.solver = PolicyIterationAgent(self.empirical_mdp, iterations=100)
            self.converged = True
            return

        # If finished epsiode
        if action == 'finish':
            #print 'finished\n\n\n'
            # Only re-solve every 10 episodes (speeds up training)
            if self.completed == self.nextUpdate:
                #print str(self.completed) + ': solving again'
                self.solver = self.solver = PolicyIterationAgent(self.empirical_mdp, iterations=100)
                self.nextUpdate *= 2
            self.completed += 1

    def chooseAction(self, state):
        ###Your Code Here :)###
        #print
        #print 'state: ', state
        #print 'old:  ', actions

        #return random.choice(filter(lambda a: (a=='north') or (a=='east') or (a=='finish'), actions))

        '''
        # Early exploration
        if self.completed < 20:
            actions = self.empirical_mdp.getPossibleActions(state)
            newActions = filter(lambda a: (a=='north') or (a=='east') or (a=='finish'), actions)
            #print 'exploring'
            return random.choice(newActions)
        '''

        if flipCoin(self.epsilon):
            #print 'random'
            return random.choice(self.empirical_mdp.getPossibleActions(state))
        else:
            #print 'policy'
            return self.solver.getAction(state)

        #return random.choice(filter(lambda a: (a=='north') or (a=='east') or (a=='finish'), actions))


class tdAgent(agent):
	
    def __init__(self, goalPosition, eps = 0.5, alp = 0.9, gam = 0.9):
        super(tdAgent, self).__init__()
        self.type = "td"
        self.goalPosition = goalPosition
        self.weights = dict()
        self.qvalues = dict()
        self.epsilon = eps
        self.alpha = alp
        self.discount = gam
        self.its = 0
        ###Your Code Here :)###
        
    def __getFeatures(self, state):
        
        pos = state.getPosition()
        return dict({'dy' : 1. / (pos[1] - self.goalPosition[1] + 1),
                     'dx' : 1. / (self.goalPosition[0] - pos[0] + 1),
                     state.getTerrainType() : 1})
        
    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(state)
        
        if not actions:
            return 0.0
            
        return max(self.getQValue(state, action) for action in actions)
                    
    def getLegalActions(self, state):
        return self.actions

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state)

        if not actions:
            return None

        return max(actions, key = lambda action: self.getQValue(state, action) + random.uniform(-.001,0))

    def getAction(self, state):
        return random.choice(self.getLegalActions(state)) if flipCoin(self.epsilon) else self.computeActionFromQValues(state)

    def getQValue(self, state, action):
        features = self.__getFeatures(state)
#        print features
        return sum(self.weights.get(feature,0) * features[feature] for feature in features.keys())

    def update(self, state, terrainType, action, nextState, reward, nextActions):
        ###Your Code Here :)###
        p = False if True else not (self.its % 5000)
            
        self.its += 1
    
        features = self.__getFeatures(state)
#        self.actions = filter(lambda action : action not in ['west', 'south'], nextActions)
        self.actions = nextActions
        difference = reward + \
                     self.discount * self.computeValueFromQValues(nextState) - \
                     self.getQValue(state, action)
                     
        #print features
        if p:
            print
            print self.weights
        self.weights.update((feature, self.weights.get(feature,0) + \
                             self.alpha * difference * features[feature])
                            for feature in features.keys())
        if p:
            print self.weights
            print
    def chooseAction(self, actions, state, terrainType):
        ###Your Code Here :)###
#        self.actions = filter(lambda action : action not in ['west', 'south'], actions)
        self.actions = actions
        return self.getAction(state)
        

