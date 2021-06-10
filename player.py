from panda3d.core import Vec2, Vec3, Vec4
from panda3d.core import Plane, Point3

# Class to create players and store player specific information

from marble import *

class Player(object):
    def __init__ (self, name):
        self.name = name
        self.captured = {2: [], 1: [], 0: []} #, 2-black, 1-gray, 0-white
        # store last mouse position when mouse is outside window
        self.lastMousePos = Vec2(0, 0)
        # plane where mouse selections occur
        self.boardPlane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))
        self.selectedMarble = None

    def addCapturedMarble(self, marble):
        self.captured[marble.color].append(marble)

    def removeCapturedMarble(self, color):
        if self.captured[color] != []:
            marble = self.captured[color].pop()
        return marble
    
    def selectMarble(self, marble):
        self.selectedMarble = marble
    
    def releaseMarble(self):
        self.selectedMarble = None
 
    def restartSavedPlayer(self, quantity):
        marbles = {}
        colors = [0, 1, 2] # white, gray, black
        for color in colors:
            marbles[color] = []
            for i in range(quantity[color]):
                newMarble = Marble(color, (0, 0, 500))
                marbles[color].append(newMarble)
        self.captured = marbles

    def clearCaptured(self):
        print("here")
        for color in self.captured:
            print(self.captured)
            print(self.captured[color])
            for marble in self.captured[color]:
                print(marble)
                marble.removeMarble()

    # passes mouse events to turn object
    def update(self, keyMap):
        mouseWatcher = base.mouseWatcherNode
        if mouseWatcher.hasMouse():
            mousePos = mouseWatcher.getMouse() # window coordinates
        else:
            mousePos = self.lastMousePos
        mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()
        base.camLens.extrude(mousePos, nearPoint, farPoint)
        self.boardPlane.intersectsLine(mousePos3D,
                            render.getRelativePoint(base.camera, nearPoint),
                            render.getRelativePoint(base.camera, farPoint))

        cell = base.board.inCell(mousePos3D)        
        pool = base.board.inPool(mousePos3D)        
        capt = base.board.inCaptured(mousePos3D, self)

        # update turn on mouse click
        if keyMap["select"]: # left mouse button
            base.turn.update(self, pool=pool, capt=capt, cell=cell)
        if keyMap["deselect"]: # right mouse button
            base.turn.deselect(self)

        # save in case mouse moves out of window
        self.lastMousePos = mousePos


        ##############################################
        # helpful debugging code
        if (cell != None):
            ring = base.board.boardState[cell]["ring"]
            marble = base.board.boardState[cell]["marble"]
            ringState = base.board.boardState[cell]["free"]
            # jumps = base.board.openJumps(cell)
            # print(jumps)
            # print(f'{cell} : r={ring}, m={marble}, f={ringState}')
            pass
        elif (pool != None):
            # print(f'pool={pool}')
            pass
        elif (capt != None):
            # print(f'captured={zone}')
            pass



