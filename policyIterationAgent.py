#
#  Policy Iteration
#
#  Purpose: Solve MDP using value iteration
#
#  Author: Willie Boag
#


from collections import defaultdict
import random

import numpy
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg

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
            newValues = self.linalg_policyEvaluation(policy, values, iterations=50)
            #newValues = self.policyEvaluation(policy, values, iterations=200)

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


        for state in self.mdp.getStates():
            if state.getWorld() == 0:
                print state, '\t', values[state]

        exit()

        return values


    def linalg_policyEvaluation(self, policy, values, iterations=50):

        # Separate states into different worlds
        all_states = policy.keys()
        states0 = filter(lambda s:s.getWorld() == 0, all_states)
        states1 = filter(lambda s:s.getWorld() == 1, all_states)
        states2 = filter(lambda s:s.getWorld() == 2, all_states)

        all_values = {}

        states_list = [states0,states1,states2]

        for states in states_list:

            indices = { state:i  for  i,state  in enumerate(states) }

            # Build three matrices to solve (one for each world)
            n = range(len(states1))
            mat = [ [ 0 for _ in n ] for __ in n ]
            b   = [ 0 for _ in n ]

            # Enter each linear equation into the table
            for state in states:

                # Action under a given policy
                action = policy[state]

                # Subtract from both sides of Bellman equations
                mat[indices[state]][indices[state]] -= 1

                # Each entry in the matrix
                for sPrime,prob in self.mdp.getTransitionStatesAndProbs(state,action):

                    # Subtract each constant terms from both sides of Bellman equations
                    # Note: technically, rewards come just from the state you leave so these are all the same
                    b[indices[state]] -= prob * self.mdp.getReward(state,action,sPrime)

                    # matrix entry (i,j) is the coefficient of variable j in equation i
                    mat[indices[state]][indices[sPrime]] += self.discount * prob

            # Convert b into a column vector
            b = [ [v] for v in b ]

            # Convert to matrices
            mat_A = scipy.sparse.csr_matrix(mat)
            vec_b = scipy.sparse.csr_matrix(b)

            # Solve linear system of equations
            x = scipy.sparse.linalg.spsolve(mat_A, vec_b)


            # Extract values
            values = {}
            for state in states:
                values[state] = x[indices[state]]

            all_values.update(values)

        return all_values


    def getAction(self, state):
        return self.policy[state]
