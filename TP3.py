'''
15-112 Term Project
Spring '20

Michael Stesney
mstesney

Zertz 3D
Game design based entirely on Zertz board game by Kris Burm
http://www.gipf.com/zertz/index.html

Tutorials used to learn basics of Panda3D:
https://docs.panda3d.org/1.10/python/introduction/tutorial/index
https://arsthaumaturgis.github.io/Panda3DTutorial.io/

Also used this tutorial to learn about the GUI:
https://grimfang-studio.org/data/books/book1/Panda3D%20Book%201.pdf

All other Panda3D know how gleaned from docs.panda3d.org
'''

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task # required for globalClock to work
from direct.interval.LerpInterval import *
from direct.gui.DirectGui import *

from panda3d.core import WindowProperties
from panda3d.core import Vec2, Vec3, Vec4
from panda3d.core import Plane, Point3
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight

import math
import sys
import json

from player import *
from robot import *
from board import *
from menu import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # set window size
        properties = WindowProperties()
        properties.setSize(800, 600)
        self.win.requestProperties(properties)

        # create menus
        self.menu = Menu()
        self.menu.startMenu.show()

        # no mouse camera control
        self.disableMouse()

        # create board
        self.board = Board()

        # set start camera position - move to game play
        self.startCameraPos()

        # create player - move this to game play
        self.currentPlayer = None

        # create turn
        self.turn = Turn()

        # set key map
        self.keyMap = {
            "left"      : False,
            "right"     : False,
            "up"        : False,
            "down"      : False,
            "select"    : False,
            "deselect"    : False,
            "save"      : False
        }

        # set key events
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("o", self.updateKeyMap, ["save", True])
        self.accept("o-up", self.updateKeyMap, ["save", False])
        self.accept("mouse1", self.updateKeyMap, ["select", True])
        self.accept("mouse1-up", self.updateKeyMap, ["select", False])
        self.accept("mouse3", self.updateKeyMap, ["deselect", True])
        self.accept("mouse3-up", self.updateKeyMap, ["deselect", False])

        # rotate from player2 position to player1 position
        self.cameraToPlayer1 = LerpFunc(self.swingCamera,
                                fromData = -90,
                                toData = 90,
                                duration = 1.0,
                                blendType = 'easeInOut')

        # rotate from player1 position to player2 position
        self.cameraToPlayer2 = LerpFunc(self.swingCamera,
                                fromData = 90,
                                toData = -90,
                                duration = 1.0,
                                blendType = 'easeInOut')

        # task manager list
        self.updateTask = self.taskMgr.add(self.update, "update")

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt() # time delta

        # camera movements
        deg = 25
        radius = 300
        if self.keyMap["left"]:
            self.rotateCamera(deg*dt, radius)
        if self.keyMap["right"]:
            self.rotateCamera(-deg*dt, radius)
        if self.keyMap["up"]:
            self.raiseCamera(-deg*dt, radius)
        if self.keyMap["down"]:
            self.raiseCamera(deg*dt, radius)
        if self.keyMap["save"]:
            print("save")
            self.saveGameState()

        if self.currentPlayer != None:
            self.currentPlayer.update(self.keyMap)

        # call update again
        return task.cont
    
    def swapPlayer(self):
        self.checkWin(self.currentPlayer)
        if (self.currentPlayer == self.player1):
            self.currentPlayer = self.player2
            self.cameraToPlayer2.start()
        else:
            self.currentPlayer = self.player1
            self.cameraToPlayer1.start()

    def checkWin(self, player): # 4, 5, 6
        if (len(player.captured[0]) >= 3 or
            len(player.captured[1]) >= 3 or
            len(player.captured[2]) >= 3 or
            (len(player.captured[0]) >= 3 and
             len(player.captured[1]) >= 3 and
             len(player.captured[2]) >= 3)):
            if self.menu.gameOverScreen.isHidden():
                self.menu.gameOverScreen.show()
                self.menu.winnerLabel["text"] = player.name + " Wins!"
                self.menu.winnerLabel.setText()

    def startOnePlayer(self):
        self.player1 = Player("Player 1")
        self.player2 = Robot("Player 2")
        self.currentPlayer = self.player1
        self.playGame()
    
    def startTwoPlayer(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.currentPlayer = self.player1
        self.playGame()

    def restartNewGame(self):
        self.player1.clearCaptured()
        self.player2.clearCaptured()
        base.board.startNewGame()
        self.player1 = Player("Player 1")
        if isinstance(self.player2, Robot):
            self.player2 = Robot("Player 2")
        else:
            self.player2 = Player("Player 2")
        self.currentPlayer = self.player1
        self.cameraToPlayer1.start()
        self.playGame()

    def restartSavedGame(self):
        player, robot, player1Marbles, player2Marbles = self.loadGameState()
        self.player1 = Player("Player 1")
        if (robot == True):
            self.player2 = Robot("Player 2")
        else:
            self.player2 = Player("Player 2")
        if player == "Player 1":
            self.currentPlayer = self.player1
        else:
            self.currentPlayer = self.player2
        self.player1.clearCaptured()
        self.player2.clearCaptured()
        self.player1.restartSavedPlayer(player1Marbles)
        self.player2.restartSavedPlayer(player2Marbles)
        base.board.updateCaptured(self.player1)
        base.board.updateCaptured(self.player2)
        base.board.updateCapturedArea(self.player1)
        base.board.updateCapturedArea(self.player2)
        self.playGame()

    def playGame(self):
        self.menu.hideGameOverScreen()
        self.menu.hideStartMenu()
        self.menu.hideStartMenuBackdrop()

    def endGame(self):
        base.userExit()

    def saveGameState(self):
        gameState = dict()
        gameState["currentPlayer"] = self.currentPlayer.name
        if isinstance(self.player2, Robot):
            gameState["robotPlayer"] = True
        else:
            gameState["robotPlayer"] = False
        gameState["player1Marbles"] = self.countMarbles(self.player1.captured)
        gameState["player2Marbles"] = self.countMarbles(self.player2.captured)
        gameState["poolMarbles"] = self.countMarbles(base.board.poolMarbles)
        gameState["board"] = base.board.boardState
        path = "gameState.json"
        self.writeJson(path, gameState)

    def countMarbles(self, marbles):
        newDict = dict()
        for key in marbles:
            newDict[key] = len(marbles[key])
        return newDict

    def writeJson(self, path, contents):
        with open(path, "w") as f:
            json.dump(contents, f, indent=4)
    
    def readJson(self, path):
        with open(path) as f:
            data = json.load(f)
        return data

    def loadGameState(self):
        path = "gameState.json"
        gameState = self.readJson(path)
        # set board
        board = gameState["board"]
        poolMarbles = list(gameState["poolMarbles"].values())
        base.board.restartSavedBoard(board, poolMarbles)
        # set players
        player1Marbles = list(gameState["player1Marbles"].values())
        player2Marbles = list(gameState["player2Marbles"].values())
        robot = gameState["robotPlayer"]
        player = gameState["currentPlayer"]
        return player, robot, player1Marbles, player2Marbles

    def startCameraPos(self):
        radius = 300
        angle = 90 # 6 o'clock
        polar = 45
        x, y, z = self.calcNewCameraPos(radius, angle, polar)
        self.camera.setPos(x, y, z)
        self.camera.lookAt(0, 0, 0)

    def swingCamera(self, angle, radius = 300):
        polar = 90 + self.camera.getP()
        x, y, z = self.calcNewCameraPos(radius, angle, polar)
        self.camera.setPos(x, y, z)
        self.camera.lookAt(0, 0, 0)
        return Task.cont

    def rotateCamera(self, degInc, radius):
        angle = 90 - self.camera.getH() 
        angle += degInc
        polar = 90 + self.camera.getP()
        x, y, z = self.calcNewCameraPos(radius, angle, polar)
        self.camera.setPos(x, y, z)
        self.camera.lookAt(0, 0, 0)
        return Task.cont
    
    def raiseCamera(self, degInc, radius):
        angle = 90 - self.camera.getH()
        polar = 90 + self.camera.getP()
        polar += degInc
        if (polar > 65):
            polar = 65
        elif (polar < 0):
            polar = 0
        x, y, z = self.calcNewCameraPos(radius, angle, polar)
        self.camera.setPos(x, y, z)
        self.camera.lookAt(0, 0, 0)        
        return Task.cont

    def calcNewCameraPos(self, radius, angle, polar):
        # formulas from wolfram mathworld
        x = radius * (math.cos(math.radians(angle)) *
                        math.sin(math.radians(polar)))
        y = -radius * (math.sin(math.radians(angle)) *
                        math.sin(math.radians(polar)))
        z = radius * (math.cos(math.radians(polar)))
        return (x, y, z)

game = Game()
game.run()



