#
#  Empirical MDP
#
#  Purpose: Estimate MDP based on empirical observations of transitions and rewards
#
#  Author: Willie Boag
#


from collections import defaultdict
from state import state

class EmpiricalMDP:

    def __init__(self, all_qstate_results, skills):

        # Parameters
        self.alpha = 0.5

        # Empirical estimate of transition model
        # Initially assume, every q-state result is equally likely
        #all_qstate_results = list(set(all_qstate_results))
        #for it in all_qstate_results:
        #    print it
        #exit()
        counts = defaultdict(lambda:defaultdict(lambda:{}))
        for state,action,nextState in all_qstate_results:
            counts[state][action][nextState] = 1
            #print state
        self.frequencies = counts
        '''
        global state
        mypoop = state((0,9),0)
        print '\n\n\n'
        print 'aaaa'
        print mypoop
        print 'zzzz'
        print '---'
        print counts[mypoop]
        print '---'
        print '\n\n\n'
        exit()
        '''


        # Inferred skills
        self.skills = skills

        # empirical values
        self.values = {}
        for state in self.getStates():
            self.values[state] = 0


    def getPossibleActions(self, state):
        """
        Returns list of valid actions for 'state'.

        Note that you can request moves into walls and
        that "exit" states transition to the terminal
        state under the special action "done".
        """
        #print state
        #print 'actions: ', self.frequencies[state].keys()
        return self.frequencies[state].keys()


    def getSuccessors(self, state):
        """
         following transtion function will either put you in adjacent state or keep you in same state
        """
        retVal = []
        for action in self.frequencies[state]:
            retVal += self.frequencies[state][action].keys()
        return list(retVal)


    def getStates(self):
        """
        Return list of all states.
        """
        return self.frequencies.keys()


    def getReward(self, state, action, nextState):
        #print help(state)
        #print 'pos: ', state.getPosition()
        if state.getPosition() == (9,0):
            return 1000
        else:
            x,y = state.getPosition()
            return x + y


    def isTerminal(self, state):
        """
        Only the TERMINAL_STATE state is *actually* a terminal state.
        The other "exit" states are technically non-terminals with
        a single action "exit" which leads to the true terminal state.
        This convention is to make the grids line up with the examples
        in the R+N textbook.
        """
        return (self.frequencies[state].keys() == ['finish'])


    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        if action not in self.getPossibleActions(state):
            raise "Illegal action!"

        # Empircal evidence (frequencies)
        candidates = self.frequencies[state][action].items()

        # Normalize into distribution
        n = float(sum(self.frequencies[state][action].values()))
        normed = [ (nextState,prob/n) for nextState,prob in candidates ]

        return normed


    def updateTransition(self, state, action, nextState, reward, terrain):
        assert (self.frequencies[state][action][nextState] != 0)
        self.frequencies[state][action][nextState] += 1

        # Update empirical reward
        self.values[state] = (1 - self.alpha) * self.values[state]   +     \
                                  self.alpha  * reward
