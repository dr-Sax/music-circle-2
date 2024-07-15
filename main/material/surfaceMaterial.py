from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class SurfaceMaterial(BasicMaterial):

    def __init__(self, properties = {}, lineColor = [1.0, 1.0, 1.0]):
        super().__init__(lineColor = lineColor)

        # render vertices as surface
        self.settings['drawStyle'] = GL_TRIANGLES
        # render both sides? default: front side only (vertices ordered counterclockwise)
        self.settings['doubleSide'] = False
        # render triangles as a wireframe?
        self.settings['wireframe'] = False

        # line thickness for wireframe rendering
        self.settings['lineWidth'] = 1
        self.setProperties(properties)

    def updateRenderSettings(self):
        if self.settings['doubleSide']:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
    
        if self.settings['wireframe']:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.settings['lineWidth'])
