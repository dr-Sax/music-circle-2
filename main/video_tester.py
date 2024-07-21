##########################################################
# TITLE: Spelling Circle                                 #
# AUTHOR: Nicolas Romano                                 #
# Date: 7/12/2024                                        #
# Reference: https://wordunscrambler.me/unscramble/      #
##########################################################

# https://www.tobias-erichsen.de/software/loopmidi.html
# https://www.reddit.com/r/midi/comments/ue9wc4/how_can_i_use_one_midi_device_for_two_programs/?rdt=38508

###############################################
# Package Imports                             #
###############################################
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.input import Input
from core.texture import Texture

from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial

from geometry.polygonGeometry import PolygonGeometry
from geometry.rectangleGeometry import RectangleGeometry

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
class Test(Base):

    def initialize(self):

        # View Setup
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, 0, Z]) 
        self.renderer.render(self.scene, self.camera) 
        self.clip = VideoFileClip(f'alphabet/bubbles.mp4')

        mpk_name = mido.get_input_names()
        print(mpk_name)
        self.inport = mido.open_input(mpk_name[0])


        mpk_name = mido.get_output_names()
        print(mpk_name)
        self.outport = mido.open_output(mpk_name[2])
    

    # frame updater
    def update(self):

        msg = self.inport.poll()
        if msg is not None:
            self.outport.send(msg)
            x = msg.note / 10
        else:
            x = 0

        square_geo = RectangleGeometry(
            width = 5,
            height = 5
        )

        
        current_frame = self.clip.get_frame(t = self.time)
        frame_surface = pygame.surfarray.make_surface(current_frame.swapaxes(0, 1))

        grid = Texture(frame_surface)
        grid_material = TextureMaterial(grid)
        mesh = Mesh(square_geo, grid_material) 
        mesh.translate(x = x, y = 0, z = 0)

        self.scene.add(mesh)
       
        self.renderer.render(self.scene, self.camera)

        self.scene.remove(mesh)
        
        



def func1():
    Test(screenSize = [WIDTH, HEIGHT]).run()

def func2():
    s = Server()
    print(pm_list_devices())
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

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()

