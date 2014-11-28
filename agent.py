#-------------------------------------------------------------------------------
# Name:        agent.py
#
# Purpose:     Agent object.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------



class Agent:

    def __init__(self):
        raise Exception('cannot instantiate Agent base class')

    def startEpisode(self):
        raise Exception('must overload Agent::startEpisode() in derived class')

    def stopEpisode(self):
        raise Exception('must overload Agent::stopEpisode() in derived class')

    def getAction(self, state):
        raise Exception('must overload Agent::getAction() in derived class')

    def observeTransition(self, state, action, nextState, reward):
        raise Exception('must overload Agent::observeTransition() in derived class')

