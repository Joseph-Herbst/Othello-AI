from __future__ import division

import time
import math
import random


def dumbPolicy(state):

    while not state.isTerminal():
        choices1 = state.getPossibleActions()
        if choices1 != []:
            best = [None,-64]
            for board in choices1:
                test = move(self.board.array,board[0],board[1],state.board.player)
                score = 0
                for x in range(8):
                        for y in range(8):
                                if test[x][y]==None:
                                    pass
                                if test[x][y]=="b":
                                    score+=1
                                else:
                                    score-=1
                if score >= best[1]:
                    best = [board,score]
            state = state.takeAction(best)
        else:
            state.board.player = 1-state.board.player
            ##############################
        choices2 = state.getPossibleActions()
        if choices2 != []:
            action = random.choice(choices2)
            state = state.takeAction(action)
        else:
            state.board.player = 1
        if choices1 == [] and choices2 == []:
            state.isTerminal = True
    return state.getReward()

def randomPolicy(state):
    while not state.isTerminal():
        choices1 = state.getPossibleActions()
        if choices1 != []:
            action = random.choice(choices1)
            state = state.takeAction(action)
        state.board.player = 0
        choices2 = state.getPossibleActions()
        if choices2 != []:
            action = random.choice(choices2)
            state = state.takeAction(action)
        state.board.player = 1
        if choices1 == [] and choices2 == []:
            state.isTerminal = True
    return state.getReward()



class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        if actions ==[]:
            return node
        for action in actions:
            if action not in node.children.keys():
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode
        print(actions)
        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action
