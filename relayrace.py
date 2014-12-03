####
#
# Relay Race
# Jake Kinsman
# 11/28/2014
#
####

import terrain as Terrain
import state as State
import agent as Agent
import gameworld as Gameworld
import graphics as Graphics

import copy
import random
from collections import defaultdict

class relayRace(object):
	
	def __init__(self):
		self.world = Gameworld.gameWorld()
		self.highScores = defaultdict(lambda: 0)
		self.tdRaceOrder = list()
		self.adpRaceOrder = list()
		self.randomRaceOrder = list()
		for _ in range(3):
			self.world.addAgent(Agent.adpAgent(self.world))
			self.world.addAgent(Agent.tdAgent())
			self.world.addAgent(Agent.randomAgent())
	
	#tested
	def trainAgents(self, numIter):
		for index, terrain in enumerate(self.world.terrains):

			for training in range(numIter):
				for tdAgent in self.world.tdAgents:
					self.world.setAgentState(tdAgent, self.world.getStartState(index))
					movements = list()
					score = 0
					while not self.world.completedRace(self.world.getAgentState(tdAgent), index):
						actions = self.world.getActions(self.world.getAgentState(tdAgent))
						action = tdAgent.chooseAction(actions)
						self.world.moveAgent(tdAgent, self.world.getAgentState(tdAgent), action)
						movements.append(self.world.getAgentState(tdAgent))
						tdAgent.update()
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(tdAgent, state) * (self.world.discount ** ind))
					#print score
					if score > self.highScores[(tdAgent.type, tdAgent.index, index)]:
						self.highScores[(tdAgent.type, tdAgent.index, index)] = score

				for adpAgent in self.world.adpAgents:
					self.world.setAgentState(adpAgent, self.world.getStartState(index))
					movements = list()
					score = 0
					while not self.world.completedRace(self.world.getAgentState(adpAgent), index):
						actions = self.world.getActions(self.world.getAgentState(adpAgent))
						action = tdAgent.chooseAction(actions)
						self.world.moveAgent(adpAgent, self.world.getAgentState(adpAgent), action)
						movements.append(self.world.getAgentState(adpAgent))
						adpAgent.update()
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(adpAgent, state) * (self.world.discount ** ind))
					#print score
					if score > self.highScores[(adpAgent.type, adpAgent.index, index)]:
						self.highScores[(adpAgent.type, adpAgent.index, index)] = score

				for randomAgent in self.world.randomAgents:
					self.world.setAgentState(randomAgent, self.world.getStartState(index))
					movements = list()
					score = 0
					while not self.world.completedRace(self.world.getAgentState(randomAgent), index):
						actions = self.world.getActions(self.world.getAgentState(randomAgent))
						action = tdAgent.chooseAction(actions)
						self.world.moveAgent(randomAgent, self.world.getAgentState(randomAgent), action)
						movements.append(self.world.getAgentState(randomAgent))
						randomAgent.update()
					for ind, state in enumerate(movements):
						if self.world.completedRace(state, 0):
							score += (self.world.transitionalReward * (self.world.discount ** ind))
						elif self.world.completedRace(state, 2):
							score += (self.world.terminalReward * (self.world.discount ** ind))
						else:
							score += (self.world.getReward(randomAgent, state) * (self.world.discount ** ind))
					#print score
					if score > self.highScores[(randomAgent.type, randomAgent.index, index)]:
						self.highScores[(randomAgent.type, randomAgent.index, index)] = score
	#tested
	def arrangeTeam(self):
		
		adpHighScore, adpArrangement = 0, list()
		tdHighScore, tdArrangement = 0, list()
		randomHighScore, randomArrangement = 0, list()

		for i, agentI in enumerate(self.world.adpAgents):
			for j, agentJ in enumerate(self.world.adpAgents):
				for k, agentK in enumerate(self.world.adpAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > adpHighScore:
							adpHighScore = score
							adpArrangement = [i, j, k]


		for i, agentI in enumerate(self.world.tdAgents):
			for j, agentJ in enumerate(self.world.tdAgents):
				for k, agentK in enumerate(self.world.tdAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > tdHighScore:
							tdHighScore = score
							tdArrangement = [i, j, k]

		
		for i, agentI in enumerate(self.world.randomAgents):
			for j, agentJ in enumerate(self.world.randomAgents):
				for k, agentK in enumerate(self.world.randomAgents):
					####
					if i != j and j != k and i != k:
						agentIScore = self.highScores[(agentI.type, agentI.index, 0)]
						agentJScore = self.highScores[(agentJ.type, agentJ.index, 1)]
						agentKScore = self.highScores[(agentK.type, agentK.index, 2)]
						score = agentIScore + agentJScore + agentKScore
						if score > randomHighScore:
							randomHighScore = score
							randomArrangement = [i, j, k]
		
		self.adpRaceOrder = adpArrangement
		self.tdRaceOrder = tdArrangement
		self.randomRaceOrder = randomArrangement
		print "adp: ", adpArrangement, adpHighScore
		print "td: ", tdArrangement, tdHighScore
		print "random: ", randomArrangement, randomHighScore

	#tested
	def race(self):
		
		randomStates = list()
		adpStates = list()
		tdStates = list()
		randomScores = list()
		adpScores = list()
		tdScores = list()
		
		#Race TD Agents
		for index, agentRef in enumerate(self.randomRaceOrder):
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.randomAgents[agentRef])
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(actions)
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			randomStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			randomScores.append(score)

		#Race ADP Agents
		for index, agentRef in enumerate(self.adpRaceOrder):
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.adpAgents[agentRef])
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(actions)
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			adpStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			adpScores.append(score)

		#Race TD Agents
		for index, agentRef in enumerate(self.tdRaceOrder):
			racingAgentMovements = list()
			racingAgent = self.world.getWorldAgent(self.world.tdAgents[agentRef])
			self.world.setAgentState(racingAgent, self.world.getStartState(index))
			while not self.world.completedRace(self.world.getAgentState(racingAgent), index):
				actions = self.world.getActions(self.world.getAgentState(racingAgent))
				action = racingAgent.chooseAction(actions)
				self.world.moveAgent(racingAgent, self.world.getAgentState(racingAgent), action)
				racingAgentMovements.append(self.world.getAgentState(racingAgent))
			tdStates.append(racingAgentMovements)
			score = 0
			for ind, state in enumerate(racingAgentMovements):
				if self.world.completedRace(state, 0):
					score += (self.world.transitionalReward * (self.world.discount ** ind))
				elif self.world.completedRace(state, 2):
					score += (self.world.terminalReward * (self.world.discount ** ind))
				else:
					score += (self.world.getReward(racingAgent, state) * (self.world.discount ** ind))
			tdScores.append(score)

		return [randomStates, adpStates, tdStates, randomScores, adpScores, tdScores], self

a = relayRace()
print "TRAINING AGENTS..."
print ""
a.trainAgents(100)
a.arrangeTeam()
print "\nRACING AGENTS..."
print ""
results, race = a.race()
print "First RAND AGENT: \t", results[0][0][len(results[0][0]) - 1], "\t", results[3][0]
print "Second RAND AGENT: \t", results[0][1][len(results[0][1]) - 1], "\t", results[3][1]
print "Third RAND AGENT: \t", results[0][2][len(results[0][2]) - 1], "\t", results[3][2]
print ""
print "First ADP AGENT: \t", results[1][0][len(results[1][0]) - 1], "\t", results[4][0]
print "Second ADP AGENT: \t", results[1][1][len(results[1][1]) - 1], "\t", results[4][1]
print "Third ADP AGENT: \t", results[1][2][len(results[1][2]) - 1], "\t", results[4][2]
print ""
print "First TD AGENT: \t", results[2][0][len(results[2][0]) - 1], "\t", results[5][0]
print "Second TD AGENT: \t", results[2][1][len(results[2][1]) - 1], "\t", results[5][1]
print "Third TD AGENT: \t", results[2][2][len(results[2][2]) - 1], "\t", results[5][2]
print ""
print "BEGINNING SIMULATION:"
print ""
Graphics.simulation(results, race)
