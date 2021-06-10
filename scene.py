# Class to create board model

from panda3d.core import Material
from panda3d.core import TextureStage

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec2, Vec3, Vec4

MODEL = "/c/Panda3D-1.10.6-x64/models/myModels/scene"
TEXTURE = "/c/Panda3D-1.10.6-x64/models/myModels/tex/blue.png"

class Scene(object):
    def __init__(self):
        self.scene = self.loadScene()
        self.updateTexture(TEXTURE)
        self.updateMaterial()

        # set ambient light
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.3, 0.3, 0.3, 1)) # intensity
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        # set directional light
        dLight = DirectionalLight("dlight")
        dLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        self.dLightNodePath = render.attachNewNode(dLight)
        self.dLightNodePath.setHpr(90, -70, 0)        
        render.setLight(self.dLightNodePath)
        # dLight.setShadowCaster(True, 512, 512)

        # set shader
        render.setShaderAuto()

    # load scene model and put in scene
    def loadScene(self):
        scene = loader.loadModel(MODEL)
        scene.reparentTo(render)
        scene.setPos(0, 0, 0)
        return scene

    # update texture file at load
    def updateTexture(self, path):
        tex = loader.loadTexture(path)
        self.scene.setTexture(tex, 1)        

    # create blue for scene
    def createMaterial(self):
        mat = Material("blue")
        mat.setAmbient((0.59375, 0.7578125, 0.83984375, 1))
        mat.setDiffuse((0.59375, 0.7578125, 0.83984375, 1,))
        mat.setEmission((.25, .25, .25, 1))
        mat.setShininess(64)
        mat.setSpecular((0.75, 0.75, 0.75, 1))
        mat.setLocal(True)
        return mat

    # replace model material
    def updateMaterial(self):
        newMat = self.createMaterial()
        oldMat = self.scene.findMaterial("mref1")
        self.scene.replaceMaterial(oldMat, newMat)
