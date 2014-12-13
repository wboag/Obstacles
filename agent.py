####
#
# Agents
# Jake Kinsman
# 11/28/2014
#
####

import random
from collections import defaultdict
from empiricalMDP import EmpiricalMDP
from  valueIterationAgent import ValueIterationAgent
from policyIterationAgent import PolicyIterationAgent
import time


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
		self.epsilon = 0.01
		self.alpha = 0.
		self.discount = .95

	
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


import state as State


class adpAgent(agent):
	
    def __init__(self, gameworld, all_qstate_results, discount=0.5):
        super(adpAgent, self).__init__()
        self.type = "adp"

        # Parameters
        self.epsilon = 0.4
        self.discount = discount

        # Estimate of model
        self.inferredSkills = { k:1 for k  in ['water','grass','forest','mountain'] }
        self.empirical_mdp = EmpiricalMDP(all_qstate_results, self.rewardValues, self.inferredSkills)
        start = time.time()
        self.learningAgent = PolicyIterationAgent #PolicyIterationAgent
        self.solver = self.learningAgent(self.empirical_mdp, discount=discount, iterations=50)
        end = time.time()
        '''
        for i in range(3):
            for j in range(10):
                for k in range(10):
                    state = State.state((k,j),i)
                    action = self.solver.policy[state]
                    if action == 'south' or action == 'west':
                            print '%7s' % action.upper(),
                    else:
                            print '%7s' % action,
                print
            print '\n\n'
        '''

        '''
        import pickle
        with open('opt-policy','wb') as f:
            pickle.dump(self.solver.policy, f)
        '''

        '''
        import pickle
        with open('opt-policy','rb') as f:
            opt_policy = pickle.load(f)

        if opt_policy == self.solver.policy:
            print 'good'
        else:
            print 'bad'
            for state in opt_policy.keys():
                if opt_policy[state] != self.solver.policy[state]:
                    print '\t', state, '\t', opt_policy[state], '\t', self.solver.policy[state]
        '''
        # Keep track of number of completed episodes
        self.converged = False
        self.completed = 0
        self.nextUpdate = 1


    def setEpsilon(self, epsilon):
        self.epsilon = epsilon


    def update(self, state, terrain, action, nextState, reward):
        # If already converged, then skip update
        if self.converged:
            return

        # update empirical MDP
        self.empirical_mdp.update(state, action, nextState, reward, terrain)

        # If converged AFTER most recent update, then solve MDP for final time
        if self.empirical_mdp.converged():
            self.solver = self.solver = self.learningAgent(self.empirical_mdp, discount=self.discount, iterations=50)
            self.converged = True
            return

        # If finished epsiode
        if action == 'finish':
            # Backoff how often you re-solve (speeds up training)
            if self.completed == self.nextUpdate:
                self.solver = self.solver = self.learningAgent(self.empirical_mdp, discount=self.discount, iterations=50)
                self.nextUpdate *= 2
            self.completed += 1

    def chooseAction(self, state):

        if flipCoin(self.epsilon):
            return random.choice(self.empirical_mdp.getPossibleActions(state))
        else:
            return self.solver.getAction(state)

class tdAgent(agent):
	
    def __init__(self, goalPosition, eps = 0.7, alp = 0.3, gam = 0.95):
        super(tdAgent, self).__init__()
        self.type = "td"
        self.x, self.y = goalPosition
        self.weights = dict()
        self.qvalues = dict()
        self.epsilon = eps
        self.alpha = alp
        self.discount = gam
        self.its = 0
        self.weights['finish'] = 1.0
        self.visited = defaultdict(lambda:defaultdict(lambda:0))
        self.completed = 0

    def __dirToVect(self, action):
        if action == 'north':
            return (0,-1)
        elif action == 'south':
            return (0,1)
        elif action == 'east':
            return (1,0)
        elif action == 'west':
            return (-1,0)
        else:
            return (0,0)

    def __getFeatures(self, state, action):
        x,y = state.getPosition()
        dx, dy = self.__dirToVect(action)
        next_x, next_y = x + dx, y + dy
        dy = next_y - self.y + 1
        dx = self.x - next_x + 1

        feat = {(State.state((x, y), state.getWorld()),action):1}
        return feat

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
        return max(actions, key = lambda action: self.getQValue(state, action) + random.uniform(0,.00001))

    def getAction(self, state):
        if flipCoin(self.epsilon):
            return random.choice(self.getLegalActions(state))
        else:
            return self.computeActionFromQValues(state)

    def getQValue(self, state, action):
        features = self.__getFeatures(state, action)
        return sum([self.weights.get(feature,0.) * features[feature] for feature in features.keys()])

    def __printWeights(self):
        for key, val in self.weights.items():
            print key, val
        print

    def update(self, state, terrainType, action, nextState, reward, nextActions):
        if self.visited[state][action] >= 200:
            return
        self.visited[state][action] += 1

        if action == 'finish':
            self.completed += 1

        DEBUG = 0
        p = False if not DEBUG else not (self.its % 50000)
        self.its += 1
        features = self.__getFeatures(state, action)
        self.actions = nextActions
        difference = reward + \
                     self.discount * self.computeValueFromQValues(nextState) - \
                     self.getQValue(state, action)
        if p:
            print
            self.__printWeights()
        self.weights.update((feature, self.weights.get(feature,0.) + \
                             self.alpha * difference * features[feature])
                            for feature in features.keys())
        if p:
            self.__printWeights()
            print

    def chooseAction(self, actions, state, terrainType):
        if sum([self.visited[state][action] for action in self.visited[state].keys()]) < 20:
            self.actions = filter(lambda action : action not in ['east', 'north'], actions)
            if len(self.actions) is 0:
                self.actions = filter(lambda action : action not in ['south', 'west'], actions)
        else:
            self.actions = actions
        act = self.getAction(state)
        self.oldAct = act
        return act