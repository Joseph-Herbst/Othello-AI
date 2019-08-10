#Library import
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from mcts_dumb import mcts
from stats import *

#Variable setup
running = True
value = 0


class Board:
        def __init__(self):
                #Black goes first (0 is white and player,1 is black and computer)
                self.player = 1
                self.player_score = 0
                self.computer_score = 0
                self.passed = False
                #Initializing an empty board
                self.array = []
                for x in range(8):
                        self.array.append([])
                        for y in range(8):
                                self.array[x].append(None)

                #Initializing center values
                self.array[3][3]="w"
                self.array[3][4]="b"
                self.array[4][3]="b"
                self.array[4][4]="w"

                #Initializing old values
                self.oldarray = self.array
        #Updating the board to the screen
        def update(self):
                if (self.player_score + self.computer_score) >= 64:
                        endGame()
                        return
                
                self.drawScoreBoard()
                #If the computer is AI, make a move
                if self.player==1:
                        startTime = time()
                        self.oldarray = self.array
                        mctsearch = mcts(iterationLimit=value)###########################################
                        try:
                                action = mctsearch.search(initialState=OthelloState(self.array))
                                self.array = move(self.array, action.x, action.y)
                        except IndexError:
                                self.won = True
                                endGame()
                                return
                else:      ##random player
                        choices = []
                        for x in range(8):
                                for y in range(8):
                                        if valid(board.array,0,x,y):
                                                choices.append((x,y))
                        if choices != []:
                                randmove = choice(choices)
                                board.boardMove(randmove[0],randmove[1])
                self.player = 1-self.player
                self.passTest()


        #Moves to position
        def boardMove(self,x,y):
                #Move and update screen
                self.oldarray = self.array
                self.oldarray[x][y]="w"
                self.array = move(self.array,x,y)              
 

        #METHOD: Draws scoreboard to screen
        def drawScoreBoard(self):
                #Scoring based on number of tiles
                self.player_score = 0
                self.computer_score = 0
                for x in range(8):
                        for y in range(8):
                                if self.array[x][y]==None:
                                        break
                                elif self.array[x][y]=="w":
                                        self.player_score+=1
                                elif self.array[x][y]=="b":
                                        self.computer_score+=1

        #METHOD: Test if player must pass: if they do, switch the player
        def passTest(self):
                mustPass = True
                for x in range(8):
                        for y in range(8):
                                if valid(self.array,self.player,x,y):
                                        mustPass=False
                if mustPass:
                        self.player = 1-self.player
                        if self.passed==True:
                                endGame()
                        else:
                                self.passed = True
                else:
                        self.passed = False


#FUNCTION: Returns a board after making a move according to Othello rules
#Assumes the move is valid
def move(passedArray,x,y):
        #Must copy the passedArray so we don't alter the original
        array = deepcopy(passedArray)
        #Set colour and set the moved location to be that colour
        if board.player==0:
                colour = "w"
                
        else:
                colour="b"
        array[x][y]=colour
        
        #Determining the neighbours to the square
        neighbours = []
        for i in range(max(0,x-1),min(x+2,8)):
                for j in range(max(0,y-1),min(y+2,8)):
                        if array[i][j]!=None:
                                neighbours.append([i,j])
        
        #Which tiles to convert
        convert = []

        #For all the generated neighbours, determine if they form a line
        #If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
                neighX = neighbour[0]
                neighY = neighbour[1]
                #Check if the neighbour is of a different colour - it must be to form a line
                if array[neighX][neighY]!=colour:
                        #The path of each individual line
                        path = []
                        
                        #Determining direction to move
                        deltaX = neighX-x
                        deltaY = neighY-y

                        tempX = neighX
                        tempY = neighY

                        #While we are in the bounds of the board
                        while 0<=tempX<=7 and 0<=tempY<=7:
                                path.append([tempX,tempY])
                                value = array[tempX][tempY]
                                #If we reach a blank tile, we're done and there's no line
                                if value==None:
                                        break
                                #If we reach a tile of the player's colour, a line is formed
                                if value==colour:
                                        #Append all of our path nodes to the convert array
                                        for node in path:
                                                convert.append(node)
                                        break
                                #Move the tile
                                tempX+=deltaX
                                tempY+=deltaY
                                
        #Convert all the appropriate tiles
        for node in convert:
                array[node[0]][node[1]]=colour

        return array


#Checks if a move is valid for a given array.
def valid(array,player,x,y):
        #Sets player colour
        if player==0:
                colour="w"
        else:
                colour="b"
                
        #If there's already a piece there, it's an invalid move
        if array[x][y]!=None:
                return False

        else:
                #Generating the list of neighbours
                neighbour = False
                neighbours = []
                for i in range(max(0,x-1),min(x+2,8)):
                        for j in range(max(0,y-1),min(y+2,8)):
                                if array[i][j]!=None:
                                        neighbour=True
                                        neighbours.append([i,j])
                #If there's no neighbours, it's an invalid move
                if not neighbour:
                        return False
                else:
                        #Iterating through neighbours to determine if at least one line is formed
                        valid = False
                        for neighbour in neighbours:

                                neighX = neighbour[0]
                                neighY = neighbour[1]
                                
                                #If the neighbour colour is equal to your colour, it doesn't form a line
                                #Go onto the next neighbour
                                if array[neighX][neighY]==colour:
                                        continue
                                else:
                                        #Determine the direction of the line
                                        deltaX = neighX-x
                                        deltaY = neighY-y
                                        tempX = neighX
                                        tempY = neighY

                                        while 0<=tempX<=7 and 0<=tempY<=7:
                                                #If an empty space, no line is formed
                                                if array[tempX][tempY]==None:
                                                        break
                                                #If it reaches a piece of the player's colour, it forms a line
                                                if array[tempX][tempY]==colour:
                                                        valid=True
                                                        break
                                                #Move the index according to the direction of the line
                                                tempX+=deltaX
                                                tempY+=deltaY
                        return valid


####################################################################################################################################
class OthelloState():
        def __init__(self, board):
                self.board = board

        def getPossibleActions(self):
                choices = []
                for x in range(8):
                        for y in range(8):
                                if valid(self.board,1,x,y):
                                        choices.append(Action(x,y))
                return choices
        def takeAction(self, action):
                if action.x == -1: ##take no action
                        return self.board
                else:
                        return OthelloState(move(self.board, action.x, action.y))
        def isTerminal(self):
                mustPass = True
                for x in range(8):
                        for y in range(8):
                                if valid(self.board,1,x,y):
                                        mustPass=False
                return mustPass
        def getReward(self):
                player_score = 0
                computer_score = 0
                for x in range(8):
                        for y in range(8):
                                if self.board[x][y]==None:
                                        break
                                elif self.board[x][y]=="w":
                                        player_score+=1
                                elif self.board[x][y]=="b":
                                        computer_score+=1
                return (player_score < computer_score)
                
class Action():
    def __init__(self, x, y):
##        self.player = player
        self.x = x
        self.y = y
####################################################################################################################################

def endGame():
        global board, running
        board.drawScoreBoard()
        gameOver(board.player_score <= board.computer_score)
##        print(board.player_score," ",board.computer_score)
        running = False

def playGame():
        global board, running
        board = 0

        #Create the board and update it
        board = Board()
        while running:
                board.update()

def dumb_iteration(val):
        global running,value
        running = True
        value = val
        playGame()


