#
#  Empirical MDP
#
#  Purpose: Estimate MDP based on empirical observations of transitions and rewards
#
#  Author: Willie Boag
#


from collections import defaultdict


class EmpiricalMDP:

    def __init__(self, all_qstate_results, rewardValues, skills):

        # Parameters
        self.alpha = 0.5

        # Constant rewards for each terrain type
        self.rewardValues = rewardValues

        # Empirical estimate of transition model
        # Initially, assume every q-state result is equally likely
        counts = defaultdict(lambda:defaultdict(lambda:{}))
        for state,action,nextState in all_qstate_results:
            counts[state][action][nextState] = 1
        self.frequencies = counts


        # Inferred skills
        self.skills = skills



    def getPossibleActions(self, state):
        return self.frequencies[state].keys()



    def getSuccessors(self, state):
        retVal = []
        for action in self.frequencies[state]:
            retVal += self.frequencies[state][action].keys()
        return list(retVal)



    def getStates(self):
        return self.frequencies.keys()



    def getReward(self, state, action, nextState):
        if action == 'finish':
            return 1000

        x, y = state.getPosition()
        manDist = (abs(y - 9) + abs(x - 0))

        terrain = state.getTerrainType()
        skillScore = self.skills[terrain] * self.rewardValues[terrain]

        return skillScore + manDist



    def isTerminal(self, state):
        return (self.frequencies[state].keys() == ['finish'])



    def getTransitionStatesAndProbs(self, state, action):
        if action not in self.getPossibleActions(state):
            raise "Illegal action!"

        '''
        chanceToFall = None
        chanceToSlideDown = None
        chanceToSlideLeft = None
        if terrainElement == 'grass':
            chanceToFall = abs(newAgent.skillLevels['grass'] - 1) / 4
        elif terrainElement == 'water':
            chanceToFall = abs(newAgent.skillLevels['water'] - 1) / 4
        elif terrainElement == 'forest':
            chanceToFall = abs(newAgent.skillLevels['forest'] - 1) / 4
        else:
            chanceToFall = abs(newAgent.skillLevels['mountain'] - 1) / 2
        x, y = state.getPosition()
        chanceToSlideDown = 0.1 - ((0.1 / 10) * (abs(y -  0)))
        chanceToSlideLeft = 0.1 - ((0.1 / 10) * (abs(x - 9)))
        if random.random() <= chanceToSlideDown:
            self.setAgentState(newAgent, State.state((x, min([9, y + 1])), state.getWorld()))
        elif random.random() <= chanceToSlideLeft:
            self.setAgentState(newAgent, State.state((max([x - 1, 0]), y), state.getWorld()))
        elif random.random() <= chanceToFall:
            self.setAgentState(newAgent, State.state((max([x - 1, 0]), min([9, y + 1])), state.getWorld()))
        else:
            self.setAgentState(newAgent, self.generateNextStates(state, action))
        '''

        # Empircal evidence (frequencies)
        candidates = self.frequencies[state][action].items()

        # Normalize into distribution
        n = float(sum(self.frequencies[state][action].values()))
        normed = [ (nextState,freq/n) for nextState,freq in candidates ]

        return normed



    def update(self, state, action, nextState, reward, terrain):
        # Another observation of particular outcome
        assert (self.frequencies[state][action][nextState] != 0)
        self.frequencies[state][action][nextState] += 1

        # Keep track of success on each terrain

        # Update empirical skill estimate
        # TODO: Stop udating after convergence (AKA doesnt change by .01 for 20 iterations)
        x,y = state.getPosition()
        skillScore = reward - (abs(y - 9) + abs(x - 0))
        skillSample = skillScore/self.rewardValues[terrain]
        self.skills[terrain] = (1 - self.alpha) * self.skills[terrain]   +     \
                                    self.alpha  * skillSample
        #print self.skills
