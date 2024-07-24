##########################################################
# TITLE: Triangle Surface                                #
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
from geometry.polygonGeometry import PolygonGeometry

from math import sin, cos, pi, trunc
from OpenGL.GL import *
from pyo import *
from pyo import Server
import mido
from moviepy.editor import VideoFileClip
import pygame
from threading import Thread

################################################
# Constants                                    #
################################################
WIDTH = 2560 / 2
HEIGHT = 1400 / 2
Z = 20  # Sets camera distance away from xy plane  Zoom
X = 10

# render a basic scene
class GraphicsWindow(Base):
    def initialize(self):
        # View Setup
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, 0, Z]) 
        self.renderer.render(self.scene, self.camera) 
        self.clip = VideoFileClip(f'alphabet/bubbles.mp4')

        # Connect to midi and virtual midi
        # mpk_name = mido.get_input_names()
        # #print(mpk_name)
        # self.inport = mido.open_input(mpk_name[0])
        # mpk_name = mido.get_output_names()
        # #print(mpk_name)
        # self.outport = mido.open_output(mpk_name[2])
    
    # frame updater
    def update(self):
        # msg = self.inport.poll()
        # if msg is not None:
        #     self.outport.send(msg)
        #     x = msg.note / 10
        # else:
        #     x = 0

        square_geo = PolygonGeometry(
            sides = 3,
            radius = 5
        )

        current_frame = self.clip.get_frame(t = self.time)
        frame_surface = pygame.surfarray.make_surface(current_frame.swapaxes(0, 1))

        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)
        mesh = Mesh(square_geo, grid_material) 
        mesh.translate(x = 0, y = 0, z = 0)

        self.scene.add(mesh)
        self.renderer.render(self.scene, self.camera)
        self.scene.remove(mesh)

class PyoWindow():
    def __init__():
        s = Server()
        #print(pm_list_devices())
        s.setMidiInputDevice(2)
        s.boot()
        notes = Notein(poly=10, scale=1, mul=.5)
        adsr = MidiAdsr(notes['velocity'],attack=.005,decay=.1, sustain=.4, release=1)
        ratio = Midictl(1, channel=1, mul=.5)
        index1 = Midictl(2, channel=1, mul=5)
        index2 = Midictl(3, channel=1, mul=5)
        xfm = CrossFM(carrier = notes['pitch'], ratio=ratio, ind1=index1, ind2=index2, mul=adsr).out()
        s.gui(locals())
        s.noteout(pitch=70)

def run_graphics_window():
    GraphicsWindow(screenSize = [WIDTH, HEIGHT]).run()

def run_pyo_window():
    PyoWindow()
    
if __name__ == '__main__':
    #Thread(target = run_graphics_window).start()
    #Thread(target = run_pyo_window).start()

    run_graphics_window()