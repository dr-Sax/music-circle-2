##########################################################
# TITLE: Spelling Circle                                 #
# AUTHOR: Nicolas Romano                                 #
# Date: 7/12/2024                                        #
# Reference: https://wordunscrambler.me/unscramble/      #
##########################################################

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


################################################
# Constants                                    #
################################################
WIDTH = 2560 / 2
HEIGHT = 1400 / 2
Z = 20  # Sets camera distance away from xy plane  Zoom
X = 10
TRIGGER_CIRCLE_CNT = 8
TRIGGER_CIRCLE_RAD = 3

PERIM_RAD_A = 8
PERIM_RAD_B = 8

COMBINED_WORD_Y_0 = 5
COMBINED_WORD_X_0 = 12
COMBINED_WORD_RADIUS = TRIGGER_CIRCLE_RAD * 2 / 5
COMBINED_WORD_BLOCK_SPACING = 2 * COMBINED_WORD_RADIUS

# keyboard inputs programmed to the MAKEY-MAKEY
MUSIC_CIRCLE_NOTES = ['w', 'a', 's', 'd', 'f', 'j', 'h', 'k']
ANGLE_INDEX_PITCHES = [80, 82, 84, 85, 87, 89, 91, 92]  # CMaj

# Pick for each new game
ALPHABET_BLOCKS = ['r', 'e', 'a', 'd', 'i', 'n', 'g', 's']

# render a basic scene
class Test(Base):

    def initialize(self):

        # View Setup
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([X, 0, Z])

        # Groupings of Scene Objects to be added or removed
        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]
        self.abet_answer_containter = []
        self.abet_trigger_count = [0, 0, 0, 0, 0, 0, 0, 0]
        
        # Audio Port Setup
        self.outport = mido.open_output()

        for i in range(0, TRIGGER_CIRCLE_CNT):

            x, y = self.angle_index_to_cartesian(idx = i)
            pc = self.perimeter_circle_generator(x, y)
            pab = self.perimeter_alphabet_block_generator(i, x, y) 
            cwa = self.combined_word_arrangement_generator(i)

            self.scene.add(pc)
            self.scene.add(pab)   
            self.scene.add(cwa)       
            
            self.renderer.render(self.scene, self.camera) 

    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP):
        material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 12,
                'drawStyle': draw_style
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [r, g, b]
        )

        return material
    
    def angle_index_to_cartesian(self, idx):
        # indexing in radians and converting to cartesian points
        theta = 2 * pi * idx / TRIGGER_CIRCLE_CNT
        x = PERIM_RAD_A * cos(theta)
        y = PERIM_RAD_B * sin(theta)
        
        return x, y
    
    def perimeter_alphabet_block_generator(self, idx, x, y, z = 0, scale = 1):
        square_geo = RectangleGeometry(
            width = scale * TRIGGER_CIRCLE_RAD * math.sqrt(2),
            height = scale * TRIGGER_CIRCLE_RAD * math.sqrt(2)
        )
        grid = Texture(f'alphabet/{ALPHABET_BLOCKS[idx]}.png')
        grid_material = TextureMaterial(grid)
        mesh = Mesh(square_geo, grid_material) 
        mesh.translate(x = x, y = y, z = z)
        
        return mesh
    
    def combined_word_arrangement_generator(self, idx):
         
        abet_geo = PolygonGeometry(
            sides = 100, 
            radius = COMBINED_WORD_RADIUS,
            x = COMBINED_WORD_X_0 + idx * COMBINED_WORD_BLOCK_SPACING,
            y = COMBINED_WORD_Y_0
        ) 
        material = self.material_gen(r = 0, g = 1, b = 1)
        abet_mesh = Mesh(abet_geo, material)

        return abet_mesh
    
    def perimeter_circle_generator(self, x, y):

        # Create Geometry and Material
        trigger_circle_geometry = PolygonGeometry(
            sides = 100, 
            radius = TRIGGER_CIRCLE_RAD,
            x = x,
            y = y
            )
        trigger_circle_material = self.material_gen(r = 1, g = 0, b = 1)

        trigger_circle_mesh = Mesh(
                trigger_circle_geometry, 
                trigger_circle_material
        )
        
        return trigger_circle_mesh

    # frame updater
    def update(self):

        # make sounds only while a circle is triggered
        if len(self.input.keyPressedList) > 0:
            for key in self.input.keyDownList:
                try:
                    angle_index = MUSIC_CIRCLE_NOTES.index(key)
                    self.sound_generator(angle_idx = angle_index)
                    
                except Exception as e:
                    print(e)

        for key in self.input.keyDownList:

            pos_idx = MUSIC_CIRCLE_NOTES.index(key)
            cur_key_cnt = self.abet_trigger_count[pos_idx]

            is_last_letter_added = len(self.abet_answer_containter) == pos_idx
            cmb_wrd_idx = len(self.abet_answer_containter)

            # on first triggers:
            if cur_key_cnt == 0:
                
                self.abet_trigger_count[pos_idx] = 1
                x = COMBINED_WORD_X_0 + cmb_wrd_idx * COMBINED_WORD_BLOCK_SPACING
                y = COMBINED_WORD_Y_0

                mesh = self.perimeter_alphabet_block_generator(pos_idx, x, y, z = 0, scale = 2/5)

                self.abet_answer_containter.append(mesh)
                self.scene.add(mesh)

            elif cur_key_cnt == 1 and is_last_letter_added:
                self.abet_trigger_count[pos_idx] = 0
                removed_letter = self.abet_answer_containter.pop()
                self.scene.remove(removed_letter)

        self.renderer.render(self.scene, self.camera)

    def sound_generator(self, angle_idx, velocity = 127):

        pitch = ANGLE_INDEX_PITCHES[angle_idx]

        msg = mido.Message(
                    'note_on', 
                    note = pitch, 
                    velocity = velocity
                                )
        self.outport.send(msg)

if __name__ == '__main__':
    Test(screenSize = [WIDTH, HEIGHT]).run()


