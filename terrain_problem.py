#-------------------------------------------------------------------------------
# Name:        terrain_problem.py
#
# Purpose:     Specialized problem object with terrain states to contain rules for actions.
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


from problem import Problem


class TerrainProblem(Problem):

    rock = 'r'
    grass = 'g'
    water = 'w'
    terminalState = 'terminal-state'

    def __init__(self, grid=None):
        if grid == None:
            r = TerrainProblem.rock
            g = TerrainProblem.grass
            w = TerrainProblem.water
            grid = [ [g,w,w,w], [g,'#',w,-1], [w,w,w,1]]
        self.grid = grid
        self.startState = (0,0)

    def getStartState(self):
        return self.startState

    def getReward(self, state, action, nextState):
        if state == TerrainProblem.terminalState:
            return 0.0
        x, y = state
        cell = self.grid[x][y]
        if (type(cell) == int) or (type(cell) == float):
            return cell
        return 0

    def getPossibleActions(self, state):
        if state == TerrainProblem.terminalState:
            return []
        x,y = state
        if type(self.grid[x][y]) == int:
            return ('exit',)
        actions = ['north', 'south', 'east', 'west']
        retVal = [ a for a in actions if isLegalAction(self.grid, state, a) ]
        return retVal

    def getNextState(self, state, action):
        x,y = state

        cell = self.grid[x][y]
        if (type(cell) == int) or (type(cell) == float):
            return TerrainProblem.terminalState

        if not isLegalAction(self.grid, state, action):
            return state
        else:
            if action == 'north':
                return (x+1,y  )
            if action == 'south':
                return (x-1,y  )
            if action == 'east':
                return (x  ,y+1)
            if action == 'west':
                return (x  ,y-1)




def isLegalAction(grid, state, action):
    x,y = state

    if action == 'north':
        return (x+1 < len(grid   )) and (grid[x+1][y  ] != '#')
    if action == 'south':
        return (x-1 >=           0) and (grid[x-1][y  ] != '#')
    if action == 'east':
        return (y+1 < len(grid[0])) and (grid[x  ][y+1] != '#')
    if action == 'west':
        return (y-1 >=           0) and (grid[x  ][y-1] != '#')

    return False

