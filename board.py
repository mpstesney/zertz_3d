# Class to create board and hold all the board state information

from direct.showbase.ShowBase import ShowBase
from direct.interval.LerpInterval import *

from panda3d.core import Vec2, Vec3, Vec4
from panda3d.core import Plane, Point3
import json

from scene import *
from marble import *
from ring import *
from player import *
from turn import *

class Board():
    def __init__(self):
        # load scene
        scene = Scene()
        # load dicts of cell coordinates and cell neighbors
        self.cellDict = self.createBoardCellPosDict()
        self.neighborDict = self.createCellNeighborsDict()
        # dict with state of all board positions
        self.boardState = self.initializeBoard()
        # rings on board
        self.rings = []
        self.setRings()
        # marbles in pool
        self.poolMarbles = self.createMarbles([6, 8, 10])
        self.updatePool() # set pool locations
        self.poolArea = {0 : None, 1 : None, 2 : None}
        self.updatePoolArea()
        # marbles on board
        self.boardMarbles = []
        # players' captured marbles
        self.capturedArea = self.initCapturedArea()
        # all current open jumps on board
        self.jumps = []
    
    # load cell position dictionary 
    def createBoardCellPosDict(self):
        path = "cellPositions.json"
        data = base.readJson(path)
        posDict = {}
        for key in data:
            coords = data[key]
            posDict[key] = Vec3(coords[0], coords[1], coords[2])
        return posDict

    # load cell neighbors dictionary
    def createCellNeighborsDict(self):
        path = "cellNeighbors.json"
        return base.readJson(path)

    # set up initial state of board
    def initializeBoard(self):
        stateDict = {}
        for cell in self.cellDict:
            stateDict[cell] = {
                "ring" : True,
                "marble" : None,
                "free" : False
            }
        return stateDict

    # reset board for restart
    def resetBoard(self):
        for ring in self.rings:
            ring.removeRing()
        for color in self.poolMarbles:
            for marble in self.poolMarbles[color]:
                marble.removeMarble()
        for marble in self.boardMarbles:
            marble.removeMarble()
        self.boardState = {}

    # reset for new game after game completion
    def startNewGame(self):
        self.resetBoard()
        self.boardState = self.initializeBoard()
        self.rings = []
        self.setRings()
        self.poolMarbles = self.createMarbles([6, 8, 10])
        self.updatePool()
        self.updatePoolArea()
        self.boardMarbles = []
        self.capturedArea = self.initCapturedArea()
        self.jumps = []

    # set up board from saved game
    def restartSavedBoard(self, board, poolMarbles):
        self.resetBoard()
        self.boardState = board
        self.rings = []
        self.setRings()
        self.poolMarbles = self.createMarbles(poolMarbles)
        self.updatePool() # set pool locations
        self.updatePoolArea()
        # populate marbles on board
        for cell in self.boardState:
            if self.boardState[cell]["marble"] != None:
                color = self.boardState[cell]["marble"]
                newMarble = Marble(color, (0, 0, 500))
                height = 6 # set on ring
                self.boardMarbles.append(newMarble)
                newMarble.setPos(self.cellDict[cell] + (0, 0, height))
                newMarble.setCell(cell)
        self.updateJumps()                

    # place rings in game state position
    def setRings(self):
        for cell in self.boardState:
            self.addRing(cell)
        self.updateFreeRings()
        
    # add ring to board
    def addRing(self, cell):
        if (self.boardState[cell]["ring"] == True):
            newRing = Ring(self.cellDict[cell], cell)
            self.rings.append(newRing)

    # returns true if ring exists and is open
    def isOpenRing(self, cell):
        if (self.boardState[cell]["ring"] == False):
            return False
        elif ((self.boardState[cell]["ring"] == True) and
            (self.boardState[cell]["marble"] == None)):
        # elif (self.boardState[cell]["marble"] == None):
            return True
        else:
            return False
    
    # update free status of all rings on board
    def updateFreeRings(self):
        for cell in self.boardState:
            self.boardState[cell]["free"] = self.isFreeRing(cell)

    # determine if ring is free to remove
    def isFreeRing(self, cell):
        if (self.boardState[cell]["ring"] == False):
            return False
        neighbors = self.neighborDict[cell]
        for i in range(len(neighbors)):
            n1 = neighbors[i]
            n2 = neighbors[(i + 1) % len(neighbors)]
            if ((n1 == None or self.boardState[n1]["ring"] == False) and
                (n2 == None or self.boardState[n2]["ring"] == False)):
                return True
        return False
    
    # check for isolated single rings
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

    # populate pool marbles from list of quantities
    def createMarbles(self, quantity):
        marbles = {}
        colors = [0, 1, 2] # white, gray, black
        for color in colors:
            marbles[color] = []
            for i in range(quantity[color]):
                newMarble = Marble(color, (0, 0, 500))
                marbles[color].append(newMarble)
        return marbles

    # return marble object at given cell
    def getMarble(self, cell):
        for marble in self.boardMarbles:
            if marble.getCell() == cell:
                return marble
        return None

    # return total number of marbles in pool
    def poolMarblesNum(self):
        count = 0
        for key in self.poolMarbles:
            count += len(self.poolMarbles[key])
        return count 

    # update pool marble positions
    def updatePool(self):
        xCenter = 88
        w = 11
        z = 5
        for color in self.poolMarbles:
            if (self.poolMarbles[color] != []):
                numMarbles = len(self.poolMarbles[color])
                x = xCenter - (color * w)
                y = (numMarbles - 1) * 11 / 2
                for i in range(numMarbles):
                    pos = Vec3(x, y, z)
                    self.poolMarbles[color][i].setPos(pos)
                    y -= 11

    # update selection area of pool
    def updatePoolArea(self):
        xCenter = 88
        w = 11
        for color in self.poolMarbles:
            x = xCenter - (color * w)
            x1 = x - w/2
            x2 = x + w/2
            yLength = len(self.poolMarbles[color])
            y1 = (yLength / 2) * w
            y2 = -(yLength / 2) * w
            self.poolArea[color] = (x1, x2, y1, y2)

    # update captured marble positions
    def updateCaptured(self, player):
        captured = player.captured
        total = 0
        marbles = []
        for color in captured:
            total += len(captured[color])
            for marble in captured[color]:
                marbles.append(marble)
        side = -1
        if (player.name == "Player 2"):
            side = 1
        h = 5
        w = 11
        y = 77 * side
        if (total % 2 == 0):
            startX = ((total / 2 * w) - w / 2) * side
        else:
            startX = (total // 2 * w) * side
        if (total != 0):
            for i in range(total):
                x = startX - (w * i) * side
                marbles[i].setPos(Vec3(x, y, h))

    # dictionary containing selection areas of captured marbles
    def initCapturedArea(self):
        areaDict = {"Player 1" : {0 : None, 1 : None, 2 : None},
                    "Player 2" : {0 : None, 1 : None, 2 : None}}
        return areaDict

    # update selection area of captured marbles
    def updateCapturedArea(self, player):
        captured = player.captured
        total = 0
        for color in captured:
            total += len(captured[color])
            if color == 0:
                white = len(captured[color])
            elif color == 1:
                gray = len(captured[color])
            else:
                black = len(captured[color])
        if (player.name == "Player 1"):
            self.p1CapturedArea(total, white, gray, black)
        else:
            self.p2CapturedArea(total, white, gray, black)

    # update player1 captured marble area
    def p1CapturedArea(self, total, white, gray, black):
        w = 11
        yCenter = -77
        y1 = (yCenter + w / 2)
        y2 = (yCenter - w / 2)
        x1 = (total / 2 * w) * -1
        x2 = x1 + (black * w)
        x3 = x2 + (gray * w)
        x4 = x3 + (white * w)
        if (black != 0):
            blackRec = (x1, x2, y1, y2)
        else:
            blackRec = None
        if (gray != 0):
            grayRec = (x2, x3, y1, y2)
        else:
            grayRec = None
        if (white != 0):
            whiteRec = (x3, x4, y1, y2)
        else:
            whiteRec = None
        self.capturedArea["Player 1"][0] = whiteRec
        self.capturedArea["Player 1"][1] = grayRec
        self.capturedArea["Player 1"][2] = blackRec

    # update player2 captured marble area
    def p2CapturedArea(self, total, white, gray, black):
        w = 11
        yCenter = 77
        y1 = (yCenter + w / 2)
        y2 = (yCenter - w / 2)
        x1 = (total / 2 * w) * -1
        x2 = x1 + (white * w)
        x3 = x2 + (gray * w)
        x4 = x3 + (black * w)
        if (white != 0):
            whiteRec = (x1, x2, y1, y2)
        else:
            whiteRec = None
        if (gray != 0):
            grayRec = (x2, x3, y1, y2)
        else:
            grayRec = None
        if (black != 0):
            blackRec = (x3, x4, y1, y2)
        else:
            blackRec = None
        self.capturedArea["Player 2"][0] = whiteRec
        self.capturedArea["Player 2"][1] = grayRec
        self.capturedArea["Player 2"][2] = blackRec

    # return cell id if mouse in cell
    def inCell(self, pos):
        cellRadius = 9.0
        for cell in self.cellDict:
            mouseX = pos[0]
            mouseY = pos[1]
            cellX = self.cellDict[cell].x
            cellY = self.cellDict[cell].y
            dist = ((cellX - mouseX)**2 + (cellY - mouseY)**2)**0.5
            if (dist < cellRadius):
                return cell
        return None
    
    # return pool color id if mouse in pool
    def inPool(self, pos):
        colors = [0, 1, 2] # white, gray, black
        for color in self.poolArea:
            if self.inRec(pos, self.poolArea[color]):
                return color
        return None
    
    # return color id if mouse in captured marble zone
    def inCaptured(self, pos, player):
        if self.inRec(pos, self.capturedArea[player.name][0]):
            return 0
        elif self.inRec(pos, self.capturedArea[player.name][1]):
            return 1
        elif self.inRec(pos, self.capturedArea[player.name][2]):
            return 2        
        return None

    # determine if point w/in rectangle (left x, right x, top y, bottom y)
    def inRec(self, pos, rec):
        if rec == None:
            return False
        elif (pos[0] > rec[0] and pos[0] < rec[1] and
            pos[1] < rec[2] and pos[1] > rec[3]):
            return True
        return False

    # determine single jumps from a cell    
    def openJumps(self, cell):
        neighbors = self.neighborDict[cell]
        jumps = []
        for dir in range(len(neighbors)): # six 
            nbr = neighbors[dir]
            if (nbr != None) and (self.boardState[nbr]["marble"] != None):
                target = self.neighborDict[nbr][dir]
                if (target != None) and (self.isOpenRing(target)):
                    jump = {"cell" : cell,
                            "capture" : nbr,
                            "target" : target}
                    jumps.append(jump)
        return jumps
    
    # return list of dictionaries of all open jumps on board
    def updateJumps(self):
        cells = []
        for cell in self.boardState:
            if self.boardState[cell]["marble"] != None:
                cells.append(cell)
        # find all single jumps from marbles on board
        jumps = []
        for cell in cells:
            j = self.openJumps(cell)
            jumps.extend(j)
        self.jumps = jumps

#####################
# player moves
#####################
    
    # select marble from pool
    def selectMarble(self, color, player):
        marble = self.poolMarbles[color][0]
        player.selectMarble(marble)
    
    # select marble from captured
    def selectCapturedMarble(self, color, player):
        marble = player.captured[color][0]
        player.selectMarble(marble)

    # place selected marble on board
    def placeMarble(self, cell, marble):
        height = 6 # set on ring
        if (self.isOpenRing(cell) == True):
            self.boardState[cell]["marble"] = marble.getColor()
            self.boardMarbles.append(marble)
            marble.setPos(self.cellDict[cell] + (0, 0, height))
            marble.setCell(cell)
            self.lastMarble = marble
            self.updateJumps()

    # move marble during jump
    def moveMarble(self, fromCell, toCell, marble):
        height = 6 # set on ring
        self.boardState[fromCell]["marble"] = None
        self.boardState[toCell]["marble"] = marble.getColor()
        marble.setPos(self.cellDict[toCell] + (0, 0, height))
        # self.jumpAction(marble, toCell)
        marble.setCell(toCell)
        self.updateJumps()
    
    # remove marble from pool after placement on board
    def removePoolMarble(self, marble):
        color = marble.getColor()
        self.poolMarbles[color].pop(0)
        self.updatePool()
        self.updatePoolArea()

    # remove marble from captured after placement on board
    def removeCapturedMarble(self, marble, player):
        color = marble.getColor()
        player.captured[color].pop(0)
        self.updateCapturedArea(player)
        self.updateCapturedArea(player)

    # move marble from board to player's captured marbles
    def captureMarble(self, cell, player):
        capturedMarble = self.getMarble(cell)
        capturedMarble.setCell(None)
        self.boardMarbles.remove(capturedMarble)
        self.boardState[cell]["marble"] = None
        player.addCapturedMarble(capturedMarble)
        self.updateCaptured(player)
        self.updateCapturedArea(player)
        self.updateJumps()
    
    # remove ring from board
    def removeRing(self, cell):
        for ring in self.rings:
            if ring.getCell() == cell:
                self.rings.remove(ring)
                self.boardState[cell]["ring"] = False
                ring.removeRing()
                self.updateFreeRings()
                self.updateJumps()
