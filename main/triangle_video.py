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
        self.phi = 0
        self.pause_iter = 0
    
    def get_height(self, base, side):
        height = np.sqrt(side ** 2 - (base / 2) ** 2)
        return height
    
    def get_cur_video_frame(self, current_time):
        current_frame = self.clip.get_frame(t = current_time)
        frame_surface = pygame.surfarray.make_surface(current_frame.swapaxes(0, 1))
        return frame_surface
    
    def get_triangle_mesh(self, vid_tstamp, base, phi, x, y, grid_material):
        side = base / TRIANGLE_WH_P
        height = self.get_height(base, side)
        geometry = IsoscelesTriangleGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh
    
    def get_square_mesh(self, vid_tstamp, base, phi, x, y, grid_material):
        geometry = RectangleGeometry(width = base, height = base)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh

    def get_parallelogram_mesh(self, vid_tstamp, base, height, phi, x, y, grid_material):
        geometry = ParallelogramGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh
    
    def draw_house(self, b1, grid_material, phi):
        s1 = b1 / TRIANGLE_WH_P
        h1 = self.get_height(b1, s1)
        x1 = X0 + h1 / (2 * np.sqrt(2))
        y1 = Y0
        theta = 3 * np.pi / 4 + phi

        TA1_mesh = self.get_triangle_mesh(self.time, b1, theta, x1 + 10*np.sin(self.phi/100*2*np.pi), y1 + 10*np.sin(self.phi/100*2*np.pi), grid_material)
        x2 = X0 - h1 / (2 * np.sqrt(2))
        y2 = Y0
        theta = 5 * np.pi / 4 + phi
        TA2_mesh = self.get_triangle_mesh(self.time, b1, theta, x2, y2, grid_material)

        b2 = s1
        s2 = s1 / TRIANGLE_WH_P
        s3 = s2 / TRIANGLE_WH_P
        y3 = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        x3 = X0 + h1 / (2 * np.sqrt(2))
        theta = 0 + phi
        TB_mesh = self.get_triangle_mesh(self.time, b2, theta, x3, y3, grid_material)

        xS = X0 - s3
        yS = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        theta = 0 + phi
        S_mesh = self.get_square_mesh(self.time, s3, theta, xS, yS, grid_material)

        b3 = s2
        h3 = self.get_height(b3, s3)
        x4 = xS + s3 / 2 + h3 / (2 * np.sqrt(2))
        y4 = Y0 - h1 / (2 * np.sqrt(2)) - h3 / (2 * np.sqrt(2))
        theta = np.pi / 4 + phi
        TC1_mesh = self.get_triangle_mesh(self.time, b3, theta, x4, y4, grid_material)

        x5 = x3 + s3 - h3 / (2 * np.sqrt(2))
        y5 = y4
        theta = -np.pi / 4 + phi
        TC2_mesh = self.get_triangle_mesh(self.time, b3, theta, x5, y5, grid_material)

        x6 = x1 + h1 / (2 * np.sqrt(2))
        y6 = y1 + h1 / (2 * np.sqrt(2)) + b3 / 2
        theta = np.pi / 2 + phi
        P_mesh = self.get_parallelogram_mesh(self.time, b3, h3, theta, x6, y6, grid_material)

        mesh_list = [TA1_mesh, TA2_mesh, S_mesh, TB_mesh, TC1_mesh, TC2_mesh, P_mesh]

        return mesh_list
    
    def draw_raven(self, b1, grid_material, phi):
        s1 = b1 / TRIANGLE_WH_P
        b2 = s1
        s2 = s1 / TRIANGLE_WH_P
        h2 = self.get_height(b2, s2)
        s3 = s2 / TRIANGLE_WH_P
        h1 = self.get_height(b1, s1)
        b3 = s2
        h3 = self.get_height(b3, s3)

        ta1x = X0
        ta1y = Y0
        theta = 0
        TA1_mesh = self.get_triangle_mesh(self.time, b1, theta, ta1x, ta1y, grid_material)

        sx = ta1x + b3
        sy = ta1y
        theta = np.pi / 4
        S_mesh = self.get_square_mesh(self.time, s3, theta, sx, sy, grid_material)

        tc1x = ta1x + b3 / 2
        tc1y = ta1y - h1 / 2 - h3 / 2
        theta = np.pi
        TC1_mesh = self.get_triangle_mesh(self.time, b3, theta, tc1x, tc1y, grid_material)

        ta2x = tc1x + b1 / 2
        ta2y = sy - h1 / 2
        theta = 0
        TA2_mesh = self.get_triangle_mesh(self.time, b1, theta, ta2x, ta2y, grid_material)

        tc2x = tc1x + b3 / 2
        tc2y = tc1y - h3
        theta = np.pi
        TC2_mesh = self.get_triangle_mesh(self.time, b3, theta, tc2x, tc2y, grid_material)

        tbx = tc1x
        tby = tc1y - h3 / 2 - h2 / 2
        theta = 0
        TB_mesh = self.get_triangle_mesh(self.time, b2, theta, tbx, tby, grid_material)

        px = ta2x + s3
        py = ta2y - h1 / 2 - s3 / 2
        theta = 3 * np.pi / 2 + np.pi / 4
        P_mesh = self.get_parallelogram_mesh(self.time, b3, h3, theta, px, py, grid_material)

        mesh_list = [TA1_mesh, TA2_mesh, S_mesh, TC1_mesh, TC2_mesh, TB_mesh, P_mesh]

        return mesh_list


    # frame updater
    def update(self):
        frame_surface = self.get_cur_video_frame(self.time)
        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)

        b1 = 4 * np.sin(self.time)  + 12

        if self.phi == 100:
            if self.pause_iter == 20:
                self.phi = 0
                self.pause_iter = 0
            else:
                self.pause_iter += 1
        else:
            self.phi += 1

        #mesh_list = self.draw_house(b1, grid_material, self.phi / 100 * 2*np.pi)
        mesh_list = self.draw_raven(b1, grid_material, 0)

        for mesh in mesh_list:
            self.scene.add(mesh)

        self.renderer.render(self.scene, self.camera)

        for mesh in mesh_list:
            self.scene.remove(mesh)


if __name__ == '__main__':
    GraphicsWindow(screenSize = [WIDTH, HEIGHT]).run()