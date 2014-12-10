#
#  Policy Iteration
#
#  Purpose: Solve MDP using value iteration
#
#  Author: Willie Boag
#


from collections import defaultdict
import random



class PolicyIterationAgent:

    def __init__(self, mdp, discount=0.5, iterations=20):

        # parameters
        self.discount = discount

        # MDP
        self.mdp = mdp

        # Initial policy is random
        values = defaultdict(lambda:0)
        policy = { state:random.choice(self.mdp.getPossibleActions(state)) for state in self.mdp.getStates() }

        # Converged early?
        streak = 0

        for _ in range(iterations):
            #print '\tit: ', _

            # step one: policy evaluation
            newValues = self.policyEvaluation(policy, values, iterations=50)

            # step two one-step lookahead of expectimax
            newPolicy = {}
            for state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(state)
                newPolicy[state] = max(self.mdp.getPossibleActions(state),
                                       key=lambda a: self.computeQValue(newValues, state, a))

            diffs = 0
            for state in self.mdp.getStates():
                if policy[state] != newPolicy[state]:
                    diffs += 1

            # for next iteration
            values = newValues
            policy = newPolicy

            # Convergence?
            if diffs == 0:
                streak += 1
            else:
                streak = 0
            if streak >= 15: break

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
            #print '\t\tjt: ', _

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
                    qVal += prob * (self.mdp.getReward(state,action,sPrime) + self.discount*values[sPrime])
                newValues[state] = qVal

                # Convergence test
                diffs += abs(values[state] - newValues[state])

            values = newValues

            # Convergence?
            if diffs < .1: break

        return values



    def getAction(self, state):
        return self.policy[state]
