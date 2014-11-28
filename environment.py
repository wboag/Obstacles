#-------------------------------------------------------------------------------
# Name:        environment.py
#
# Purpose:     Data representation for AI environment.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


class Environment:

    def __init__(self, problem):
        raise Exception('cannot instantiate Environment base class')

    def reset(self):
        raise Exception('must overload Envionment::reset() in derived class')

    def getCurrentState(self):
        raise Exception('must overload Envionment::getCurrentState() in derived class')

    def getPossibleActions(selfself, state):
        raise Exception('must overload Envionment::getPossibleActions() in derived class')

    def doAction(self, action):
        raise Exception('must overload Envionment::doActions() in derived class')

    def isTerminal(self):
        state = self.getCurrentState()
        actions = self.getPossibleActions(state)
        return len(actions) == 0

