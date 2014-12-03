#
#  Value Iteration
#
#  Purpose: Solve MDP using value iteration
#
#  Author: Willie Boag
#


from collections import defaultdict


def max0(lst):
    if not lst: return 0
    return max(lst)



class ValueIterationAgent:

    def __init__(self, mdp, discount=0.5, iterations=100):

        # parameters
        self.discount = discount

        # MDP
        self.mdp = mdp

        # values
        self.values = defaultdict(lambda:0)

        # Run value iteration for specified number of iterations
        for _ in range(iterations):
            nextVals = defaultdict(lambda:0)

            # Get new value for each state
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state): continue
                # value is maximum Q-value
                nextVals[state] = max0([ self.getQValue(state,a) for a in self.mdp.getPossibleActions(state) ])

            self.values = nextVals


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # Q-value is expected value you get by committing to an action & then acting optimally
        qVal = 0
        for sPrime,prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qVal += prob * (self.mdp.getReward(state,action,sPrime) + self.discount*self.getValue(sPrime))
        return qVal


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        bestAction = None
        maxQ = float('-inf')
        for a in self.mdp.getPossibleActions(state):
            # choose action that yields highest Q-value
            qVal = self.getQValue(state, a)
            if qVal > maxQ:
                maxQ = qVal
                bestAction = a

        return bestAction


    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)


    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
