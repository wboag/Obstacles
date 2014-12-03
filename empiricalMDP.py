#
#  Empirical MDP
#
#  Purpose: Estimate MDP based on empirical observations of transitions and rewards
#
#  Author: Willie Boag
#


from collections import defaultdict


class EmpiricalMDP:

    def __init__(self, all_qstate_results, skills):

        # Parameters
        self.alpha = 0.5

        # Empirical estimate of transition model
        # Initially assume, every q-state result is equally likely
        counts = defaultdict(lambda:defaultdict(lambda:{}))
        for state,action,nestState in all_qstate_results:
            counts[state][action][nestState] = 1
        self.frequencies = counts


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
        return self.frequencies[state].keys()


    def getSuccessors(self, state):
        """
         following transtion function will either put you in adjacent state or keep you in same state
        """
        retVal = []
        for action in self.frequencies[state]:
            retVal += self.frequencies[state][action.keys()]
        return list(retVal)


    def getStates(self):
        """
        Return list of all states.
        """
        return self.frequencies.keys()


    def getReward(self, state, action, nextState):
        """
        Get reward for state, action, nextState transition.

        Note that the reward depends only on the state being
        departed (as in the R+N book examples, which more or
        less use this convention).
        """
        print help(state)
        exit()


    def isTerminal(self, state):
        """
        Only the TERMINAL_STATE state is *actually* a terminal state.
        The other "exit" states are technically non-terminals with
        a single action "exit" which leads to the true terminal state.
        This convention is to make the grids line up with the examples
        in the R+N textbook.
        """
        return False


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
