from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class PointMaterial(BasicMaterial):

    def __init__(self, properties = {}, lineColor = [1.0, 1.0, 1.0]):
        super().__init__(lineColor = lineColor)

        # render vertices as points
        self.settings['drawStyle'] = GL_POINTS
        # WIDTH AND HEIGHT OF POINTS, IN PIXELS
        self.settings['pointSize'] = 8
        # DRAW POINTS AS ROUNDED
        self.settings['roundedPoints'] = False

        self.setProperties(properties)

    def updateRenderSettings(self):

        glPointSize(self.settings['pointSize'])

        if self.settings['roundedPoints']:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)