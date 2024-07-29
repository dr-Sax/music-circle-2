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
WIDTH = 1400 / 2
HEIGHT = 2560 / 2
Z = 40  # Sets camera distance away from xy plane  Zoom
X = 10  # MIDDLE

# Tangram Proportions
TRIANGLE_WH_P = 8.5 / 12
Y0 = 2
X0 = 5

# render a basic scene
class GraphicsWindow(Base):
    def initialize(self):
        # View Setups
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, 0, Z]) 
        self.renderer.render(self.scene, self.camera) 
        self.clips = [VideoFileClip(f'media/cartoon_house.mp4'), 
                      VideoFileClip(f'media/eyes.mp4'), 
                      VideoFileClip(f'media/fire.mp4'), 
                      VideoFileClip(f'media/frog.mp4'),
                      VideoFileClip(f'media/shark.mp4'),
                      VideoFileClip(f'media/nosferatu.mp4')
                      ]
        self.house_coords = self.get_house_coordinates(X0, Y0, 15, 0)
        self.raven_coords = self.get_raven_coordinates(X0, Y0, 15, 0)
        
        # animation controls
        self.phi = 0
        self.pause_iter = 0
        self.direction = -1
        self.pause_period = 30
        self.scramble_period = 100
        self.iter = 0
        self.texture_list = []
        self.random_ints = []

    def screen_recorder(self, file_name):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        screen_surf = pygame.transform.flip(screen_surf, True, True)
        pygame.image.save(screen_surf, f"media/raven_house/{file_name}.jpg")

    def get_cur_video_frame(self, current_time, clip):
        
        current_frame = clip.get_frame(t = current_time)
        frame_surface = pygame.surfarray.make_surface(current_frame.swapaxes(0, 1))
        return frame_surface
    
    def get_height(self, base, side):
        height = np.sqrt(side ** 2 - (base / 2) ** 2)
        return height
    
    def get_triangle_mesh(self, coords, grid_material):
        base, phi, x, y = coords
        side = base / TRIANGLE_WH_P
        height = self.get_height(base, side)
        geometry = IsoscelesTriangleGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh
    
    def get_square_mesh(self, coords, grid_material):
        base, phi, x, y = coords
        geometry = RectangleGeometry(width = base, height = base)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh

    def get_parallelogram_mesh(self, coords, grid_material):
        base, height, phi, x, y = coords
        geometry = ParallelogramGeometry(base = base, height = height)
        mesh = Mesh(geometry, grid_material)  
        mesh.translate(x = x, y = y, z = 0)
        mesh.rotateZ(phi)
        return mesh
    
    def get_house_coordinates(self, X0, Y0, scale, rotation):

        # [base_length, phi, x, y]
        tangram_coords = {'ta1': (), 'ta2': (), 'tb': (), 'tc1': (), 'tc2': (), 's': (), 'p': ()}

        # Dimensions of each shape:
        b1 = scale
        s1 = b1 / TRIANGLE_WH_P
        b2 = s1
        s2 = s1 / TRIANGLE_WH_P
        h2 = self.get_height(b2, s2)
        s3 = s2 / TRIANGLE_WH_P
        h1 = self.get_height(b1, s1)
        b3 = s2
        h3 = self.get_height(b3, s3)

        ta1x = X0 + h1 / (2 * np.sqrt(2))
        ta1y = Y0
        tangram_coords['ta1'] = (b1, 3 * np.pi / 4 + rotation, ta1x, ta1y)

        sx = X0 - s3
        sy = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        tangram_coords['s'] = (s3, 0 + rotation, sx, sy)

        tc1x = sx + s3 / 2 + h3 / (2 * np.sqrt(2))
        tc1y = Y0 - h1 / (2 * np.sqrt(2)) - h3 / (2 * np.sqrt(2))
        tangram_coords['tc1'] = (b3, np.pi / 4 + rotation, tc1x, tc1y)

        ta2x = X0 - h1 / (2 * np.sqrt(2))
        ta2y = Y0
        tangram_coords['ta2'] = (b1, 5 * np.pi / 4 + rotation, ta2x, ta2y)

        tbx = X0 + h1 / (2 * np.sqrt(2))
        tby = Y0 - h1 / (2 * np.sqrt(2)) - s3 / 2
        tangram_coords['tb'] = (b2, 0 + rotation, tbx, tby)
        
        tc2x = tbx + s3 - h3 / (2 * np.sqrt(2))
        tc2y = tc1y
        tangram_coords['tc2'] = (b3, -np.pi / 4 + rotation, tc2x, tc2y)
        
        px = ta1x + h1 / (2 * np.sqrt(2))
        py = ta1y + h1 / (2 * np.sqrt(2)) + b3 / 2
        tangram_coords['p'] = (b3, h3, np.pi / 2 + rotation, px, py)

        return tangram_coords
    
    def get_raven_coordinates(self, X0, Y0, scale, rotation):

        # [base_length, phi, x, y]
        tangram_coords = {'ta1': (), 'ta2': (), 'tb': (), 'tc1': (), 'tc2': (), 's': (), 'p': ()}

        # Dimensions of each shape:
        b1 = scale
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
        tangram_coords['ta1'] = (b1, 0 + rotation, ta1x, ta1y)

        sx = ta1x + b3
        sy = ta1y
        tangram_coords['s'] = (s3, np.pi / 4 + rotation, sx, sy)

        tc1x = ta1x + b3 / 2
        tc1y = ta1y - h1 / 2 - h3 / 2
        tangram_coords['tc1'] = (b3, np.pi + rotation, tc1x, tc1y)

        ta2x = tc1x + b1 / 2
        ta2y = sy - h1 / 2
        tangram_coords['ta2'] = (b1, 0 + rotation, ta2x, ta2y)

        tbx = tc1x
        tby = tc1y - h3 / 2 - h2 / 2
        tangram_coords['tb'] = (b2, 0 + rotation, tbx, tby)
        
        tc2x = tc1x + b3 / 2
        tc2y = tc1y - h3
        tangram_coords['tc2'] = (b3, np.pi + rotation, tc2x, tc2y)
        
        px = ta2x + s3
        py = ta2y - h1 / 2 - s3 / 2
        tangram_coords['p'] = (b3, h3, 7 * np.pi / 4 + rotation, px, py)

        return tangram_coords
    
    def get_transition_coords(self, coord1, coord2, cur_time, period):
        transition_coords = {'ta1': (), 'ta2': (), 'tb': (), 'tc1': (), 'tc2': (), 's': (), 'p': ()}
        for key in transition_coords.keys():
            if key == 'p':
                b1, h1, r1, x1, y1 = coord1[key]
                b2, h2, r2, x2, y2 = coord2[key]
            else:
                b1, r1, x1, y1 = coord1[key]
                b2, r2, x2, y2 = coord2[key]

            if cur_time != period:
                t = (cur_time % period) / period
            else:
                t = cur_time / period

            rt = r1 + (r2 - r1) * t
            xt = x1 + (x2 - x1) * t
            yt = y1 + (y2 - y1) * t
            bt = b1 + (b2 - b1) * t

            if key == 'p':
                ht = h1 + (h2 - h1) * t
                transition_coords[key] = (bt, ht, rt, xt, yt)
            else:
                transition_coords[key] = (bt, rt, xt, yt)
            
        return transition_coords

    def get_tangram_mesh(self, tangram_coords):
        
        
        self.texture_list = []
        for vid in self.clips:
            
            frame_surface = self.get_cur_video_frame(self.time % vid.duration, vid)
            grid = Texture(frame_surface)
            grid_material = TextureMaterial(grid)
            self.texture_list.append(grid_material)

        if self.phi in [0, 100] and self.pause_iter in [0, 1]:
            self.random_ints = []
            for i in range(0, 7):
                self.random_ints.append(random.randint(0, len(self.clips) - 1))

        ta1_mesh = self.get_triangle_mesh(tangram_coords['ta1'], self.texture_list[self.random_ints[0]])
        ta2_mesh = self.get_triangle_mesh(tangram_coords['ta2'], self.texture_list[self.random_ints[1]])
        tb_mesh = self.get_triangle_mesh(tangram_coords['tb'], self.texture_list[self.random_ints[2]])
        tc1_mesh = self.get_triangle_mesh(tangram_coords['tc1'], self.texture_list[self.random_ints[3]])
        tc2_mesh = self.get_triangle_mesh(tangram_coords['tc2'], self.texture_list[self.random_ints[4]])
        s_mesh = self.get_square_mesh(tangram_coords['s'], self.texture_list[self.random_ints[5]])
        p_mesh = self.get_parallelogram_mesh(tangram_coords['p'], self.texture_list[self.random_ints[6]])    
       
        mesh_list = [ta1_mesh, ta2_mesh, s_mesh, tc1_mesh, tc2_mesh, tb_mesh, p_mesh]

        return mesh_list

    # frame updater
    def update(self):
        
        self.camera.setPosition([X, 0 , Z + 10 * np.sin(self.phi / self.scramble_period * np.pi)]) 
        
        if self.phi == 0 or self.phi == self.scramble_period:
            if self.pause_iter == self.pause_period:
                self.pause_iter = 0
                self.direction = self.direction * -1
                self.phi += self.direction

            else:
                self.pause_iter += 1

        else:
            self.phi += self.direction

        t_coords = self.get_transition_coords(
                                            self.house_coords,
                                            self.raven_coords,
                                            self.phi,
                                            self.scramble_period
                                            )
        
        mesh_list = self.get_tangram_mesh(t_coords)

        for mesh in mesh_list:
            self.scene.add(mesh)

        self.renderer.render(self.scene, self.camera)

        for mesh in mesh_list:
            self.scene.remove(mesh)
        
        self.screen_recorder(file_name = self.iter)
        self.iter += 1


if __name__ == '__main__':
    GraphicsWindow(screenSize = [WIDTH, HEIGHT]).run()