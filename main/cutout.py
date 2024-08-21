##########################################################
# TITLE: Parametric Surface Efficient Video              #
# AUTHOR: Nicolas Romano                                 #
# Date: 7/30/24                                          #
# Concept:
# It may be more efficient to not create and destroy
# mesh objects each time, but rather to keep a set of 7
# and update their positions and textures each update call
##########################################################

###############################################
# Package Imports                             #
###############################################
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from material.textureMaterial import TextureMaterial
from geometry.rectangleGeometry import RectangleGeometry

from math import sin, cos, pi, trunc
from OpenGL.GL import *
from pyo import *

import pygame
import numpy as np
import cv2
from shapely.geometry import Polygon

################################################
# Constants                                    #
################################################
WIDTH = 1400 / 2
HEIGHT = 2560 / 2
Z =10 # Sets camera distance away from xy plane  Zoom
X = 0  # MIDDLE
Y = 0

# Tangram Proportions
TRIANGLE_WH_P = 8.5 / 6
Y0 = 0
X0 = 0

# render a basic scene
class GraphicsWindow(Base):
    def initialize(self):
        # View Setups
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, Y, Z]) 
        self.renderer.render(self.scene, self.camera) 
        self.media_cutout = cv2.imread('media/cutout_sitting.png', cv2.IMREAD_UNCHANGED)
        self.perimeter_coords, self.edged = self.get_perimeter_coords()
        self.polygon_center, self.fmt_perimeter_coords = self.get_polygon_center()

        #print(self.draw_img())
        grid = Texture('media/cutout_sitting.png')
        grid_material = TextureMaterial(grid)
        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, grid_material)
        self.scene.add(self.mesh)

        self.renderer.render(self.scene, self.camera)

    def get_perimeter_coords(self):
        img = self.media_cutout
        alpha_channel = img[:,:,3]  # isolate alpha channel -> transparent for cutout images
        
        # Find Canny edges 
        edged = cv2.Canny(alpha_channel, 30, 200) 
        
        # Finding Contours 
        # Use a copy of the image e.g. edged.copy() 
        # since findContours alters the image 
        contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        
        # last index is the largest contour
        # cv2.imshow('Canny Edges After Contouring', edged) 
        return contours[-1], edged
    
    def get_polygon_center(self):
        fmt_perimeter_coords = []
        for i in range(0, len(self.perimeter_coords)):
            xy_coords = self.perimeter_coords[i][0]
            x = xy_coords[0]
            y = xy_coords[1]
            fmt_perimeter_coords.append((x, y))

        polygon = Polygon(fmt_perimeter_coords)
        
        return (int(polygon.centroid.x), int(polygon.centroid.y)), fmt_perimeter_coords
    
    def draw_img(self):
        img = cv2.circle(self.edged, self.polygon_center, 10, (255, 255, 255), 5, 8)
        cv2.imshow('center', img)


    def screen_recorder(self, file_name):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        screen_surf = pygame.transform.flip(screen_surf, True, True)
        pygame.image.save(screen_surf, f"media/raven_house/{file_name}.jpg")


    # frame updater
    def update(self):
        

        self.mesh.scale(1.01)
        self.renderer.render(self.scene, self.camera)
        
        # self.screen_recorder(file_name = self.iter)
        


if __name__ == '__main__':
    GraphicsWindow(screenSize = [WIDTH, HEIGHT]).run()