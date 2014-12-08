#
#  Policy Iteration
#
#  Purpose: Solve MDP using value iteration
#
#  Author: Willie Boag
#


from collections import defaultdict


def max0(lst):
    if not lst: return 0
    return max(lst)


def arg_max(func, lst):
    bestArg = None
    maxVal = float('-inf')
    for elem in lst:
        val = func(elem)
        if val > maxVal:
            maxVal = val
            bestArg = elem
    return bestArg


class PolicyIterationAgent:

    def __init__(self, mdp, discount=0.5, iterations=5):

        # parameters
        self.discount = discount

        # MDP
        self.mdp = mdp

        # Initial policy is random
        values = defaultdict(lambda:0)
        policy = { state:self.mdp.getPossibleActions(state)[0] for state in self.mdp.getStates() }

        for _ in range(iterations):

            # step one: policy evaluation
            newValues = self.policyEvaluation(policy, values, iterations)

            # step two one-step lookahead of expectimax
            newPolicy = {}
            for state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(state)
                if state.getPosition() == (8,0): save = state
                #if ('north' in actions) and ('east' in actions) and (self.computeQValue(newValues,state,'east') > self.computeQValue(newValues,state,'north')):
                #    for a in actions:
                #        print state, '\t', a, '\t', self.computeQValue(newValues,state,a)
                #    print
                #print arg_max(lambda a: self.computeQValue(newValues, state, a),
                #              self.mdp.getPossibleActions(state))

                newPolicy[state] = arg_max(lambda a: self.computeQValue(newValues, state, a),
                                           self.mdp.getPossibleActions(state))

            diffs = 0
            for state in self.mdp.getStates():
                if policy[state] != newPolicy[state]:
                    diffs += 1
                    #print state, '\t', policy[state], '\t', newPolicy[state], '\t', self.mdp.getPossibleActions(state)
            #print '\n\n'

            # for next iteration
            values = newValues
            policy = newPolicy

            # Convergence?
            if diffs == 0: break

        #print 'CONVERGED'
        #for state in self.mdp.getStates():
        #    if policy[state] != 'east':
        #        print state, '\t', policy[state], '\t', self.mdp.getPossibleActions(state)

        #print
        #for k,v in values.items():
        #    print k, '\t', v
        #exit()

        #print '\n\n'
        #state = save
        #for a in self.mdp.getPossibleActions(state):
        #    qVal = self.computeQValue(values, state, a)
        #    print '\t', state, '\t', a, '\t', qVal
        #print policy[state]
        #exit()

        # Policy
        self.policy = policy



    def computeQValue(self, values, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # Q-value is expected value you get by committing to an action & then acting optimally
        qVal = 0
        for sPrime,prob in self.mdp.getTransitionStatesAndProbs(state, action):
            #print '\t\t', sPrime, '\t', self.mdp.getReward(state,action,sPrime), '\t', values[sPrime], '\t(', prob, ')'
            qVal += prob * (self.mdp.getReward(state,action,sPrime) + self.discount*values[sPrime])
        return qVal



    def policyEvaluation(self, policy, values, iterations=50):
        # Simplified value iteration
        for _ in range(iterations):
            newValues = defaultdict(lambda:0)

            diffs = 0

            # Get new value for each state
            for state in self.mdp.getStates():
                #if self.mdp.isTerminal(state): continue

                # follow policy
                action = policy[state]

                # Compute qValue
                qVal = 0
                for sPrime,prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    #if state.getPosition() == (9,0):
                    #    print state, '\t', action, '\t', sPrime
                    qVal += prob * (self.mdp.getReward(state,action,sPrime) + self.discount*values[sPrime])
                newValues[state] = qVal

                #if state.getPosition() == (9,0): print state

                # Convergence test
                diffs += abs(values[state] - newValues[state])

            values = newValues

            # Convergence?
            if diffs < .0001: break

        return values



    def getAction(self, state):
        return self.policy[state]
