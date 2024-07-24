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
CIRCLE_CNT = 8
CIRCLE_RAD = 3
PERIM_RAD_A = 8
PERIM_RAD_B = 8

# keyboard inputs programmed to the MAKEY-MAKEY
MUSIC_CIRCLE_NOTES = ['w', 'a', 's', 'd', 'f', 'j', 'h', 'k']
ANGLE_INDEX_PITCHES = [80, 82, 84, 85, 87, 89, 91, 92]  # CMaj

def min_scale_builder(root):
    return [root, root + 2, root + 3, root + 5, root + 7, root + 8, root + 11, root + 12]

#ANGLE_INDEX_PITCHES = min_scale_builder(62) # Dmin

# render a basic scene
class Test(Base):

    def initialize(self):

        # View Setup
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])

        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]
        self.location_mesh = []
        self.outport = mido.open_output()

        # Define the Materiality of each circle position outlines on the screen
        vsCode = '''
            in vec3 vertexPosition;
            out vec3 position;
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            void main()
            {
                vec4 pos = vec4(vertexPosition, 1.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
                position = vertexPosition;
            }
        '''

        self.circle_container = []
        self.time = 0

        # Creating initial circle list
        for i in range(0, CIRCLE_CNT):

            theta = 2 * pi * i / CIRCLE_CNT
            x = PERIM_RAD_A * cos(theta)
            y = PERIM_RAD_B * sin(theta)

            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = CIRCLE_RAD,
                x = x,
                y = y
                )
            
            material = self.material_gen(r = 1, g = 0, b = 1)
            self.circle_container.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container[i])

            # # location adder:
            # self.geometry = RectangleGeometry(
            #     width = CIRCLE_RAD * math.sqrt(2),
            #     height = CIRCLE_RAD * math.sqrt(2)
            # )
        
            # grid = Texture('images/lilly_pad.png')
            # grid_material = TextureMaterial(grid)
            # mesh = Mesh(self.geometry, grid_material) 
            # mesh.translate(x = x, y=y, z = 0)
            

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
    
    # Called when a user triggers an input
    def update_note_list(self, i, t_diff = 0):
        prop = (i + 2) / CIRCLE_CNT  # repositions so that the circle starts with 1 being at 12 oclock
        theta = 2 * pi * prop  # conversion to an angle

        # decomposing into xy coordinates
        x = abs(PERIM_RAD_A - t_diff) * cos(theta)
        y = abs(PERIM_RAD_B - t_diff) * sin(theta)

        self.geometry = RectangleGeometry(
            width = CIRCLE_RAD * math.sqrt(2),
            height = CIRCLE_RAD * math.sqrt(2)
        )
        
        if i %2 == 0:
            grid = Texture('images/sonic.png')
        else:
            grid = Texture('images/amy.png')
        grid_material = TextureMaterial(grid)
        mesh = Mesh(self.geometry, grid_material) 
        mesh.translate(x = x, y=y, z = 0)

        return mesh


    # frame updater
    def update(self):
        cur_t = str(trunc(self.time * 10) / 10) 

        # clear out note circles:
        for i in self.circle_note_container:
            for j in i:
                self.scene.remove(j)
        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]

        # draw circles and create sounds
        if len(self.input.keyPressedList) > 0:

            for key in self.input.keyPressedList:
                try:
                    angle_index = MUSIC_CIRCLE_NOTES.index(key)
                    print(angle_index)
                    note_img = self.update_note_list(angle_index)
                    
                    self.circle_note_container[angle_index].append(note_img)

                    self.scene.add(note_img) # draw the note on scene
                except Exception as e:  # key is not found in list (they pressed different key other than controls)
                    print(e)

            for key in self.input.keyDownList:
                try:
                    angle_index = MUSIC_CIRCLE_NOTES.index(key)
                    self.msg = mido.Message(
                                'note_on', 
                                note = ANGLE_INDEX_PITCHES[angle_index], 
                                velocity=127
                                )
                    self.outport.send(self.msg)
                except:
                    pass
        # for img in self.location_mesh:
        #     self.scene.add(i)
        self.renderer.render(self.scene, self.camera) 
    
# instantiate this class and run the program
def func1():
    Test(screenSize = [WIDTH, HEIGHT]).run()

def func2():
    s = Server()
    s.setMidiInputDevice(1)
    s.boot()
    notes = Notein(poly=10, scale=1, mul=.5)
    adsr = MidiAdsr(notes['velocity'],attack=.005,decay=.1, sustain=.4, release=1)
    ratio = Midictl(1, channel=1, mul=.5)
    index1 = Midictl(2, channel=1, mul=5)
    index2 = Midictl(3, channel=1, mul=5)
    xfm = CrossFM(carrier = notes['pitch'], ratio=ratio, ind1=index1, ind2=index2, mul=adsr).out()
    s.gui(locals())

if __name__ == '__main__':
    
    func1()
    #Thread(target = func2).start()

# to share data between threads:
# https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

