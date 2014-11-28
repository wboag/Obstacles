#-------------------------------------------------------------------------------
# Name:        willie_agent.py
#
# Purpose:     Willie's Agent object.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


import random

from agent import Agent


class WillieAgent(Agent):

    def __init__(self, actionFn):
        self.actionFn = actionFn

    def startEpisode(self):
        pass

    def stopEpisode(self):
        pass

    def getAction(self, state):
        actions = self.actionFn(state)
        # TODO: currently random. Should somehow incorporate exploration constant
        return random.choice(actions)

    def observeTransition(self, state, action, nextState, reward):
        pass