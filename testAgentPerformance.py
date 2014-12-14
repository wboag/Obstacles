####
#
# Testing Script
# Jake Kinsman
# 11/28/2014
#
####

from relayrace import driver
import os
import sys
import commands

def test():
	scores = dict()
	scores['td'] = list()
	scores['random'] = list()
	scores['adp'] = list()
	wins = dict()
	wins['td'] = 0
	wins['adp'] = 0
	wins['random'] = 0
	for _ in range(100):
		result = driver(True, 50)
		print result
		if result['td'] == max([result['td'], result['adp'], result['random']]):
			wins['td'] += 1
		elif result['adp'] == max([result['td'], result['adp'], result['random']]):
			wins['adp'] += 1
		else:
			wins['random'] += 1
		for key in result:
			scores[key].append(result[key])
	print "Printing Wins..."
	print
	for key in wins:
		print key + ": " + str(wins[key])
	print "Printing Average Scores..."
	print
	for key in scores:
		print key + ": " + str(sum(scores[key]) / len(scores[key]))
if __name__ == '__main__':
	test()
