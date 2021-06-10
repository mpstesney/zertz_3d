# Subclass of player that contains computer player logic

import random
from player import *

class Robot(Player):
    def __init__(self, name):
        self.name = name
        self.captured = {2: [], 1: [], 0: []} #, 2-black, 1-gray, 0-white
        self.selectedMarble = None
        self.cellScore = self.createCellScoreDict()

    # robot steps match turn class steps
    def update(self, keyMap): # key map not needed
        step = base.turn.getStep()
        if step == 1: self.startTurn()
        elif step == 1.1: self.jumpStart()
        elif step == 1.2: self.jumpEnd()
        elif step == 2: self.selectMarbleToPlace()
        elif step == 3.1: self.placeFromPool()
        elif step == 3.2: self.placeFromCaptured()
        elif step == 4: self.removeRing()

    # start turn
    def startTurn(self):
        base.turn.update(self)

    # select jump start cell
    def jumpStart(self): # step 1.1
        available = base.turn.getJumpStarts()
        cell = random.choice(list(available))
        base.turn.update(self, cell=cell)

    # complete jump by selecting target cell
    def jumpEnd(self): # step 1.2
            marble = self.selectedMarble
            startCell = marble.getCell()
            targets, captures = base.turn.getJumpEnds(startCell)
            cell = random.choice(list(targets))
            base.turn.update(self, cell=cell)

    def selectMarbleToPlace(self): # step 2 
        if (base.board.poolMarblesNum != 0):
            while self.selectedMarble == None:
                color = random.randrange(len(base.board.poolMarbles)) # random selection for now
                if base.board.poolMarbles[color] != []:
                    base.turn.update(self, pool=color)
        else:
            while self.selectedMarble == None:
                color = random.randrange(len(base.board.poolMarbles)) # random selection for now
                if self.captured[color] != []:
                    base.turn.update(self, capt=color)

    def placeFromPool(self): # step 3.1 
        available = base.turn.getOpenRings()
        cell = random.choice(available) # random selection for now
        base.turn.update(self, cell=cell)

    def placeFromCaptured(self): # step 3.2
        available = base.turn.getOpenRings()
        cell = random.choice(available) # random selection for now
        base.turn.update(self, cell=cell)

    def removeRing(self): # step 4
        available = base.turn.getFreeRings()
        cell = random.choice(available) # random selection for now
        base.turn.update(self, cell=cell)
    
###################
# score positions
###################

    # scores for move choice. jump : {target : score}
    def createCellScoreDict(self):
        scoreDict = {}
        for cell in base.board.boardState:
            scoreDict[cell] = {
                            "place" : 0,
                            "jump" : {"" : 0},
                            "ring" : 0}
        return scoreDict

    # just returning list of available rings right now
    def evalPlace(self):
        available = base.turn.getOpenRings()
        for cell in available:
            score = 1
            # check for score modifiers
            if self.hasSingleFreeOpenNeighbor(cell):
                score += 10
            # assign score
            self.cellScore[cell]["place"] = score

    # just returning list of free rings right now
    def evalRing(self):
        available = base.turn.getFreeRings()
        for cell in available:
            self.cellScore[cell]["ring"] += 1        
    
    # just returning list of start jump pairs right now
    def evalJump(self):
        available = base.turn.getJumpStarts() # returns set
        for cell in available:
            targets, captures = base.turn.getJumpEnds(cell)
            for target in targets:
                self.cellScore[cell]["jump"][target] = 1
    
    # claim isolated cell during ring removal step
    def almostIsolatedMarble(self):
        pass

    # check during placement step       
    def almostIsolatedEmpty(self):
        almost = []
        openRings = base.turn.getOpenRings()
        for cell in openRings:
            if (base.board.isFreeRing(cell) and 
                self.hasSingleFreeOpenNeighbor(cell)):
                almost.append(cell)
        return almost

    # confirm that cell has single, open, free neighbor
    def hasSingleFreeOpenNeighbor(self, cell):
        if (base.board.isFreeRing(neighbor) == False):
            return False
        neighbors = self.neighborDict[cell]
        freeOpen = []
        for neighbor in neighbors:
            if (neighbor != None and
                base.board.isOpenRing(neighbor) and
                base.board.isFreeRing(neighbor)):
                freeOpen.append(neighbor)
        return (len(freeOpen) == 1)

    def getIsolatedRings(self):
        isolatedCells = []
        for cell in self.neighborDict:
            isolated = True
            if (self.boardState[cell]["ring"] == False):
                isolated = False
            else:        
                neighbors = self.neighborDict[cell]
                for neighbor in neighbors:
                    if ((neighbor != None) and 
                        (self.boardState[neighbor]["ring"] == True)):
                        isolated = False
                if (isolated == True):
                    isolatedCells.append(cell)
        return isolatedCells

# create nextBoardState to used for evaluation,
# for jump evaluation, etc
# all evaluation functions on that