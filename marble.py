# Class to create marble model

from panda3d.core import Material
from panda3d.core import TextureStage

MODEL = "/c/Panda3D-1.10.6-x64/models/myModels/marble"
TEXTURE0 = "/c/Panda3D-1.10.6-x64/models/myModels/tex/whiteSpeckle.png"
TEXTURE1 = "/c/Panda3D-1.10.6-x64/models/myModels/tex/gray.png"
TEXTURE2 = "/c/Panda3D-1.10.6-x64/models/myModels/tex/black.png"
# TEXTURE2 = "/c/Panda3D-1.10.6-x64/models/myModels/tex/Speckle White small.png"

class Marble():
    def __init__(self, color, pos, cell=None): # don't need default cell
        self.marble = self.loadMarble()
        self.color = color
        self.updateTexture(self.color)
        self.pos = pos
        self.marble.setPos(self.pos)
        self.cell = cell

    # load marble and attach nodepath
    def loadMarble(self):
        marble = loader.loadModel(MODEL)
        marble.reparentTo(render)
        return marble

    # update texture at load
    def updateTexture(self, color):
        if color == 0:
            tex = loader.loadTexture(TEXTURE0)
            mat = self.createWhite()
        elif color == 1:
            tex = loader.loadTexture(TEXTURE1)
            mat = self.createGray()            
        elif color == 2:
            tex = loader.loadTexture(TEXTURE2) 
            mat = self.createBlack()                   
        self.marble.setTexture(tex, 1)
        self.updateMaterial(mat)

    # create white material
    def createWhite(self):
        mat = Material("white")
        mat.setAmbient((1, 1, 1, 1))
        mat.setDiffuse((1, 1, 1, 1,))
        mat.setEmission((0, 0, 0, 0))
        mat.setShininess(64)
        mat.setSpecular((0.75, 0.75, 0.75, 1))
        mat.setLocal(True)
        return mat

    # create gray material
    def createGray(self):
        mat = Material("gray")
        mat.setAmbient((0.76171875, 0.76171875, 0.76171875, 1))
        mat.setDiffuse((0.76171875, 0.76171875, 0.76171875, 1,))
        mat.setEmission((0.0, 0.0, 0.0, 1))
        mat.setShininess(64)
        mat.setSpecular((0.75, 0.75, 0.75, 1))
        mat.setLocal(True)
        return mat

    # create black material
    def createBlack(self):
        mat = Material("black")
        mat.setAmbient((0.0, 0.0, 0.0, 1))
        mat.setDiffuse((0.0, 0.0, 0.0, 1,))
        mat.setEmission((0.0, 0.0, 0.0, 0.0))
        mat.setShininess(64)
        mat.setSpecular((0.75, 0.75, 0.75, 1))
        mat.setLocal(True)
        return mat

    # update model material
    def updateMaterial(self, material):
        oldMat = self.marble.findMaterial("mref1")
        self.marble.replaceMaterial(oldMat, material)

    # return marble cell location
    def getCell(self):
        return self.cell
    
    # set the marble's cell location
    def setCell(self, cell):
        self.cell = cell

    # return marble color
    def getColor(self):
        return self.color
    
    # return marble location coordinates as Vec3
    def getPos(self):
        return self.pos

    # set position of marble with Vec3
    def setPos(self, pos):
        self.pos = pos
        self.marble.setPos(self.pos)
    
    #remove marble from scene graph
    def removeMarble(self):
        self.marble.removeNode()
    


