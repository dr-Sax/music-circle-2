from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from geometry.cylinderGeometry import CylinderGeometry
from geometry.pyramidGeometry import PyramidGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from core.texture import Texture
from OpenGL.GL import *
from math import sin, cos, sqrt

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

ZOOM = 6
RADIUS = 1

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera()
        self.camera.setPosition([0, 0, ZOOM])

        geometry = SphereGeometry(radius = RADIUS, radiusSegments = 500, heightSegments = 500)
        grid = Texture('images/1.png')
        material = TextureMaterial(grid)

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)
        self.renderer.render(self.scene, self.camera)
        self.delta_x = 0.05
        self.delta_y = 0.05
        self.x_pos = 0
        self.y_pos = 0

    def update(self):
        if abs(self.delta_x + self.x_pos) >= ZOOM / 2 - RADIUS / 2:
            self.delta_x = self.delta_x * -1

        self.mesh.translate(x = self.delta_x, y = 0, z = 0)
        self.mesh.rotateY(.009)
        self.mesh.rotateX(.009)
        self.renderer.render(self.scene, self.camera)
        self.x_pos = self.x_pos + self.delta_x
        

# instantiate this class and run the program
Test(screenSize = [SCREEN_WIDTH, SCREEN_HEIGHT]).run()