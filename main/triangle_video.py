##########################################################
# TITLE: Parametric Surface Video                        #
# AUTHOR: Nicolas Romano                                 #
# Date: 7/22/2024                                        # 
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
from geometry.parallelogramGeometry import ParallelogramGeometry
from geometry.isoscelesTriangleGeometry import IsoscelesTriangleGeometry

from math import sin, cos, pi, trunc
from OpenGL.GL import *
from pyo import *
from pyo import Server
import mido
from moviepy.editor import VideoFileClip
import pygame
from threading import Thread
import numpy as np

################################################
# Constants                                    #
################################################
WIDTH = 2560 / 2
HEIGHT = 1400 / 2
Z = 20  # Sets camera distance away from xy plane  Zoom
X = 10  # MIDDLE

# Tangram Proportions
TRIANGLE_WH_P = 8.5 / 6
Y0 = -2
X0 = X

# render a basic scene
class GraphicsWindow(Base):
    def initialize(self):
        # View SetupS
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, 0, Z]) 
        self.renderer.render(self.scene, self.camera) 
        self.clip = VideoFileClip(f'alphabet/bubbles.mp4')
    
    def get_height(self, base, side):
        height = np.sqrt(side ** 2 - (base / 2) ** 2)
        return height
    
    def get_cur_video_frame(self, current_time):
        current_frame = self.clip.get_frame(t = current_time)
        frame_surface = pygame.surfarray.make_surface(current_frame.swapaxes(0, 1))
        return frame_surface
    
    def get_triangle_mesh(self, vid_tstamp, base, phi, x, y):
        frame_surface = self.get_cur_video_frame(vid_tstamp)
        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)
        side = base / TRIANGLE_WH_P
        height = self.get_height(base, side)
        geometry = IsoscelesTriangleGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        
        return mesh
    
    def get_square_mesh(self, vid_tstamp, base, phi, x, y):
        frame_surface = self.get_cur_video_frame(vid_tstamp)
        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)
        geometry = RectangleGeometry(width = base, height = base)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)

        return mesh

    def get_parallelogram_mesh(self, vid_tstamp, base, height, phi, x, y):
        frame_surface = self.get_cur_video_frame(vid_tstamp)
        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)
        geometry = ParallelogramGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)

        return mesh

    # frame updater
    def update(self):
        b1 = 16
        s1 = b1 / TRIANGLE_WH_P
        h1 = self.get_height(b1, s1)
        x1 = X0 + h1 / (2 * np.sqrt(2))
        y1 = Y0
        TA1_mesh = self.get_triangle_mesh(self.time, b1, 3 * np.pi / 4, x1, y1)
        x2 = X0 - h1 / (2 * np.sqrt(2))
        y2 = Y0
        TA2_mesh = self.get_triangle_mesh(self.time, b1, 5 * np.pi / 4, x2, y2)

        b2 = s1
        s2 = s1 / TRIANGLE_WH_P
        s3 = s2 / TRIANGLE_WH_P
        y3 = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        x3 = X0 + h1 / (2 * np.sqrt(2))
        TB_mesh = self.get_triangle_mesh(self.time, b2, 0, x3, y3)

        xS = X0 - s3
        yS = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        S_mesh = self.get_square_mesh(self.time, s3, 0, xS, yS)

        b3 = s2
        h3 = self.get_height(b3, s3)
        x4 = xS + s3 / 2 + h3 / (2 * np.sqrt(2))
        y4 = Y0 - h1 / (2 * np.sqrt(2)) - h3 / (2 * np.sqrt(2))
        TC1_mesh = self.get_triangle_mesh(self.time, b3, np.pi / 4, x4, y4)

        x5 = x3 + s3 - h3 / (2 * np.sqrt(2))
        y5 = y4
        TC2_mesh = self.get_triangle_mesh(self.time, b3, -np.pi / 4, x5, y5)

        x6 = x1 + h1 / (2 * np.sqrt(2))
        y6 = y1 + h1 / (2 * np.sqrt(2)) + b3 / 2
        P_mesh = self.get_parallelogram_mesh(self.time, b3, h3, np.pi / 2, x6, y6)

        mesh_list = [TA1_mesh, TA2_mesh, S_mesh, TB_mesh, TC1_mesh, TC2_mesh, P_mesh]
        for mesh in mesh_list:
            self.scene.add(mesh)

        self.renderer.render(self.scene, self.camera)

        for mesh in mesh_list:
            self.scene.remove(mesh)


if __name__ == '__main__':
    GraphicsWindow(screenSize = [WIDTH, HEIGHT]).run()