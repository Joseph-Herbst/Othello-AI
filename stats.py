numgame = 0
numwin = 0
totalWhite = 0
totalBlack = 0
total = 0

def gameOver(b, w):
    global numgame, numwin, totalWhite, totalBlack, total
    totalWhite+=w
    totalBlack+=b
    total+=w
    total+=b
    if b>=w:
        numwin+=1
    numgame+=1

def printResults():
    print(numwin, " / ",numgame)
    print("White: ",totalWhite)
    print("Black: ",totalBlack)
    print("Total: ",total)
    print()

def resetStats():
    global numgame, numwin
    numgame = 0
    numwin = 0
