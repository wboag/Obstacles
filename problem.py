#-------------------------------------------------------------------------------
# Name:        problem.py
#
# Purpose:     Base problem object to contain rules for actions.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------



class Problem:

    def __init__(self):
        raise Exception('cannot instantiate Problem base class')

    def getStartState(self):
        raise Exception('must overload Problem::getStartState() in derived class')

    def getPossibleActions(self, state):
        raise Exception('must overload Problem::getPossibleActions() in derived class')

