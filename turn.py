# Class that interfaces between player, including robot, and board

from panda3d.core import Vec2, Vec3, Vec4
from panda3d.core import Plane, Point3

class Turn():
    def __init__(self):
        # location in turn steps
        self.step = 1

    def getStep(self):
        return self.step

    def update(self, player, pool = None, capt = None, cell = None):
        if self.step == 1: self.startTurn()
        elif self.step == 1.1: self.jumpStart(player, cell)
        elif self.step == 1.2: self.jumpEnd(player, cell)
        elif self.step == 2: self.selectMarbleToPlace(player, pool, capt)
        elif self.step == 3.1: self.placeFromPool(player, cell)
        elif self.step == 3.2: self.placeFromCaptured(player, cell)
        elif self.step == 4: self.removeRing(player, cell)

    # check to see if there are any required jumps
    def startTurn(self):
        if (base.board.jumps == []):
            self.step = 2
            return
        else:
            self.step = 1.1
            return
   
    # select jump start cell
    def jumpStart(self, player, cell): # step 1.1
        startCells = self.getJumpStarts()
        if (cell in startCells):
            marble = base.board.getMarble(cell)
            player.selectMarble(marble)
            self.step = 1.2
            return

    # complete jump by selecting target cell
    def jumpEnd(self, player, cell): # step 1.2
            marble = player.selectedMarble
            startCell = marble.getCell()
            targets, captures = self.getJumpEnds(startCell)
            if (cell in targets):
                # move marble
                base.board.moveMarble(startCell, cell, marble)
                # capture marble
                i = targets.index(cell)
                base.board.captureMarble(captures[i], player)
                player.releaseMarble()
                # check for more jumps
                if (base.board.jumps == []):
                    self.endTurn()
                    return
                else:
                    self.step = 1.1
                    return

    # select marble from pool marbles or captured marbles
    def selectMarbleToPlace(self, player, pool, capt): # step 2
        if (base.board.poolMarblesNum() != 0) and (capt == None):
            if ((pool != None) and (player.selectedMarble == None)):
                base.board.selectMarble(pool, player)
                self.step = 3.1
                return
        else:
            if ((capt != None) and (player.selectedMarble == None)):
                base.board.selectCapturedMarble(capt, player)
                self.step = 3.2
                return    

    # place pool marble on board
    def placeFromPool(self, player, cell): # step 3.1
        if ((cell != None) and (base.board.isOpenRing(cell))):
            base.board.placeMarble(cell, player.selectedMarble)
            base.board.removePoolMarble(player.selectedMarble)
            player.releaseMarble()
            self.step = 4
            return

    # place captured marble on board
    def placeFromCaptured(self, player, cell): # step 3.2
        if ((cell != None) and (base.board.isOpenRing(cell))):
            base.board.placeMarble(cell, player, player.selectedMarble)
            base.board.removeCapturedMarble(player.selectedMarble, player)
            player.releaseMarble()
            self.step = 4
            return

    # remove ring from board
    def removeRing(self, player, cell): # step 4
        if self.getFreeRings() == []:
            self.endTurn()
        else:
            if ((cell != None) and (base.board.isOpenRing(cell)) and
                (cell in self.getFreeRings())):
                base.board.removeRing(cell)
                # check for isolated rings
                isolated = base.board.getIsolatedRings()
                if (isolated != []):
                    for cell in isolated:
                        base.board.captureMarble(cell, player)
                        base.board.removeRing(cell)
                self.endTurn()

    # complete turn, reset step, and switch players
    def endTurn(self):
        base.swapPlayer()
        self.step = 1

    # deselect marble and backup one step
    def deselect(self, player):
        if (self.step == 1.2):
            self.step = 1.1
            player.releaseMarble()
        elif ((self.step == 3.1) or (self.step == 3.2)):
            self.step = 2
            player.releaseMarble()

    # return list of all rings open for marble placement
    def getOpenRings(self):
        available = []
        for cell in base.board.boardState:
            if (base.board.isOpenRing(cell)):
                available.append(cell)
        return available

    # return list of rings free to be removed
    def getFreeRings(self):
        free = []
        for cell in base.board.boardState:
            if (base.board.isFreeRing(cell)):
                free.append(cell)
        return free    

    # return list of all possible jump start cells
    def getJumpStarts(self):
        startCells = set()
        for jump in base.board.jumps:
            startCells.add(jump["cell"])
        return startCells

    # return lists of all possible targets and captures
    # from start sell position
    def getJumpEnds(self, cell):
        targets = []
        captures = []
        for jump in base.board.jumps:
            if (jump["cell"] == cell):
                targets.append(jump["target"])
                captures.append(jump["capture"])
        return targets, captures

        