# Class that holds GUI information

from direct.gui.DirectGui import *

from direct.gui.OnscreenText import OnscreenText

COVER_IMAGE = "/c/Panda3D-1.10.6-x64/models/myModels/UI/zertz_doos.jpg"
BUTTON_1 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/1 Zertz.png"
BUTTON_2 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/2 Zertz.png"
BUTTON_HELP = "/c/Panda3D-1.10.6-x64/models/myModels/UI/Rules Zertz.png"
BUTTON_RESTART = "/c/Panda3D-1.10.6-x64/models/myModels/UI/R Zertz.png"
BUTTON_QUIT = "/c/Panda3D-1.10.6-x64/models/myModels/UI/Q Zertz.png"
BUTTON_REPLAY = "/c/Panda3D-1.10.6-x64/models/myModels/UI/R Zertz.png"
BUTTON_ARROW = "/c/Panda3D-1.10.6-x64/models/myModels/UI/Arrow Zertz.png"

GAME_RULES = "rules.txt"
RULES1 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/diagram1.gif"
RULES2 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/diagram2.gif"
RULES3 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/diagram3.gif"
RULES4 = "/c/Panda3D-1.10.6-x64/models/myModels/UI/diagram4.gif"

class Menu():
    def __init__(self):
        self.rules = self.loadRules()


        # start menu
        self.startMenuBackdrop = DirectFrame(
                            frameColor = (1, 1, 1, 1),
                            frameSize = (-1, 1, -1, 1),
                            parent = render2d,
                            frameTexture = COVER_IMAGE)
        
        self.startMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title2 = DirectLabel(
                            text = "Game design by Kris Burm",
                            scale = 0.075,
                            pos = (0, 0, -0.9),
                            parent = self.startMenu,
                            relief = None,
                            text_fg = (1, 1, 1, 1))
        
        btn = DirectButton( command = base.startOnePlayer,
                            pos = (-0.3, 0, 0.125),
                            parent = self.startMenu,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_1)
        btn.setTransparency(True)                            

        btn = DirectButton( command = base.startTwoPlayer,
                            pos = (0.3, 0, 0.125),
                            parent = self.startMenu,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_2)
        btn.setTransparency(True)                            

        btn = DirectButton( command = self.showRulesScreen,
                            pos = (0, 0, -0.175),
                            parent = self.startMenu,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_HELP)
        btn.setTransparency(True)                             

        btn = DirectButton( command = base.restartSavedGame,
                            pos = (-0.3, 0, -0.5),
                            parent = self.startMenu,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_RESTART)
        btn.setTransparency(True)                             

        btn = DirectButton( command = base.endGame,
                            pos = (0.3, 0, -0.5),
                            parent = self.startMenu,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_QUIT)
        btn.setTransparency(True)                                                                               

        # rules menu
        self.rulesScreenBackdrop = DirectFrame(
                            frameColor = (0, 0, 0, 0.2),
                            frameSize = (-1, 1, -1, 1),
                            parent = render2d)
        self.rulesScreenBackdrop.hide()
        
        self.rulesScreen = DirectScrolledFrame(
                            canvasSize = (-.6, .6, -10, .9),
                            frameSize = (-.7, .7, -.9, .9),
                            frameColor = (0, 0.258823, 0.258823, 1))
        self.rulesScreen.hide()

        rules = DirectLabel(
                            text = self.rules,
                            text_scale = 0.0525,
                            text_pos = (0, 0.75),
                            parent = self.rulesScreen.getCanvas(),
                            relief = None,
                            text_fg = (1, 1, 1, 1),
                            text_wordwrap = 22)

        btn = DirectButton( command = self.hideRulesScreen,
                            pos = (0.5, 0.675, 0.75),
                            parent = self.rulesScreen,
                            scale = 0.09,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_ARROW)
        btn.setTransparency(True)                              

        # game over screen
        self.gameOverScreen = DirectDialog(
                            frameColor = (1, 1, 1, 0),
                            frameSize = (-0.75, 0.75, -0.75, 0.7),
                            fadeScreen = 0.3,
                            relief = DGG.FLAT)

        self.gameOverScreen.hide()
        
        label = DirectLabel(
                            text = "Game Over",
                            parent = self.gameOverScreen,
                            scale = 0.2,
                            pos = (0, 0, 0.2),
                            text_fg = (1, 1, 1, 1),
                            text_bg = (1, 1, 1, 0))
        label.setTransparency(True)                            

        self.winnerLabel = DirectLabel(
                            text = "",
                            parent = self.gameOverScreen,
                            scale = 0.15,
                            pos = (0, 0, 0),
                            text_fg = (1, 1, 1, 1))

        btn = DirectButton( command = base.restartNewGame,
                            pos = (-0.3, 0, -0.2),
                            parent = self.gameOverScreen,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_ARROW)
        btn.setTransparency(True)                             

        btn = DirectButton( command = base.endGame,
                            pos = (0.3, 0, -0.2),
                            parent = self.gameOverScreen,
                            scale = 0.15,
                            frameSize = (-1, 1, -1, 1),
                            frameTexture = BUTTON_QUIT)
        btn.setTransparency(True)                                                        

    def showStartMenu(self):
        self.startMenu.show()

    def hideStartMenu(self):
        self.startMenu.hide()
    
    def hideStartMenuBackdrop(self):
        self.startMenuBackdrop.hide()

    def showGameOverScreen(self):
        self.gameOverScreen.show()

    def hideGameOverScreen(self):
        self.gameOverScreen.hide()
    
    def showRulesScreen(self):
        self.startMenu.hide()
        self.startMenuBackdrop.hide()
        self.rulesScreenBackdrop.show()
        self.rulesScreen.show()
    
    def hideRulesScreen(self):
        self.rulesScreen.hide()
        self.rulesScreenBackdrop.hide()
        self.startMenuBackdrop.show()
        self.startMenu.show()

    # from 15-112 course website
    def readFile(self, path):
        with open(path, "rt") as f:
            return f.read()
    
    def loadRules(self):
        return self.readFile(GAME_RULES)


