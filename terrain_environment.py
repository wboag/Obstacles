#-------------------------------------------------------------------------------
# Name:        terrain_environment.py
#
# Purpose:     Data representation for AI terrain environment.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


from environment import Environment


class TerrainEnvironment(Environment):

    def __init__(self, problem):
        self.problem = problem
        self.startState = self.problem.getStartState()

    def reset(self):
        self.state = self.problem.getStartState()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        return self.problem.getPossibleActions(state)

    def doAction(self, action):
        state = self.getCurrentState()
        (nextState, reward) = self.getNextState(state, action)
        self.state = nextState
        return (nextState, reward)

    def getNextState(self, state, action):
        nextState = self.problem.getNextState(state, action)
        reward = self.problem.getReward(state, action, nextState)
        return (nextState, reward)
