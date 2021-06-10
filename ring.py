# Class to create ring model

from panda3d.core import Material
from panda3d.core import TextureStage

MODEL = "/c/Panda3D-1.10.6-x64/models/myModels/ring"
TEXTURE = "/c/Panda3D-1.10.6-x64/models/myModels/tex/black.png"

class Ring():
    def __init__(self, pos, cell):
        self.ring = loader.loadModel(MODEL)
        self.ring.reparentTo(render)
        self.pos = pos
        self.ring.setPos(self.pos)
        self.cell = cell
        # self.ring.setTransparency(True)
        self.updateTexture(TEXTURE)
        self.updateMaterial()

    # update texture file at load
    def updateTexture(self, path):
        tex = loader.loadTexture(path)
        # self.ring.setTexture(tex, 1)
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        self.ring.setTexture(ts, tex)

    # create black material for ring
    def createMaterial(self):
        mat = Material("ring")
        mat.setAmbient((0, 0, 0, 1))
        mat.setDiffuse((0, 0, 0, 1))
        mat.setEmission((0, 0, 0, 1))
        mat.setShininess(115)
        mat.setSpecular((0.75, 0.75, 0.75, 1))
        mat.setLocal(True)
        return mat

    # replace model material definition
    def updateMaterial(self):
        newMat = self.createMaterial()
        oldMat = self.ring.findMaterial("mref1")
        self.ring.replaceMaterial(oldMat, newMat)

    # return ring cell location
    def getCell(self):
        return self.cell
    
    # return ring location coordinates
    def getPos(self):
        return self.pos
    
    # remove ring from scene graph
    def removeRing(self):
        self.ring.removeNode()



