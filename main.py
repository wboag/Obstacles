#-------------------------------------------------------------------------------
# Name:        main.py
#
# Purpose:     Run the main simulation for AI
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


from terrain_problem     import TerrainProblem
from terrain_environment import TerrainEnvironment
from willie_agent        import WillieAgent
from textual_display     import TextualDisplay


def main():

    # number of episodes
    episodes = 1

    # Get problem
    problem = TerrainProblem()

    # Get environment
    env = TerrainEnvironment(problem)

    # Get agent
    agent = WillieAgent(lambda state: problem.getPossibleActions(state))

    # Get display channel
    display = TextualDisplay()

    # Run episodes
    displayCallback = lambda state: display.displayValues(agent, state, "CURRENT VALUES")
    messageCallback = lambda s: printString(s)
    pauseCallback = lambda : display.pause()
    decisionCallback = agent.getAction

    returns = 0
    DISCOUNT = .5
    for episode in range(1, episodes+1):
        returns += runEpisode(agent, env, DISCOUNT, decisionCallback, displayCallback, messageCallback, pauseCallback, episode)
    if episodes > 0:
        print
        print "AVERAGE RETURNS FROM START STATE: "+str((returns+0.0) / episodes)
        print
        print


    print env
    print agent



def printString(s):
    print s


def runEpisode(agent, environment, discount, decision, display, message, pause, episode):
    returns = 0
    totalDiscount = 1.0

    environment.reset()
    if 'startEpisode' in dir(agent): agent.startEpisode()
    message("BEGINNING EPISODE: "+str(episode)+"\n")

    while True:

        # DISPLAY CURRENT STATE
        state = environment.getCurrentState()
        display(state)
        pause()

        # END IF IN A TERMINAL STATE
        actions = environment.getPossibleActions(state)
        if len(actions) == 0:
            message("EPISODE "+str(episode)+" COMPLETE: RETURN WAS "+str(returns)+"\n")
            return returns

        # GET ACTION (USUALLY FROM AGENT)
        action = decision(state)
        if action == None:
            raise 'Error: Agent returned None action'

        # EXECUTE ACTION
        nextState, reward = environment.doAction(action)
        message("Started in state: "+str(state)+
                "\nTook action: "+str(action)+
                "\nEnded in state: "+str(nextState)+
                "\nGot reward: "+str(reward)+"\n")

        # UPDATE LEARNER
        if 'observeTransition' in dir(agent):
            agent.observeTransition(state, action, nextState, reward)

        returns += reward * totalDiscount
        totalDiscount *= discount

    if 'stopEpisode' in dir(agent):
        agent.stopEpisode()



if __name__ == '__main__':
    main()