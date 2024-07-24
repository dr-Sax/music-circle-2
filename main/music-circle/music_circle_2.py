from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.polygonGeometry import PolygonGeometry
from math import sin, cos, pi, trunc
from OpenGL.GL import *
from material.surfaceMaterial import SurfaceMaterial
from pyo import *
from threading import Thread
from pynput import keyboard

WIDTH = 2560 / 2
HEIGHT = 1400 / 2
Z = 20  # Sets camera distance away from xy plane
CIRCLE_CNT = 12
CIRCLE_RAD = 1
PERIM_RAD = 10
COMBINATION = {
    keyboard.KeyCode.from_char('0'),
    keyboard.KeyCode.from_char('1'),
    keyboard.KeyCode.from_char('2'),
    keyboard.KeyCode.from_char('3'),
    keyboard.KeyCode.from_char('4'),
    keyboard.KeyCode.from_char('5'),
    keyboard.KeyCode.from_char('6'),
    keyboard.KeyCode.from_char('7'),
    keyboard.KeyCode.from_char('8'),
    keyboard.KeyCode.from_char('9'),
    keyboard.KeyCode.from_char('10'),
    keyboard.KeyCode.from_char('a')
    }

current = set()

# render a basic scene
class Test(Base):

    def initialize(self):

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])

        # Define the Materiality of each circle on the screen
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
        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]
        self.time = 0

        # Creating initial circle list
        for i in range(0, CIRCLE_CNT):

            theta = 2 * pi * i / CIRCLE_CNT
            x = PERIM_RAD * cos(theta)
            y = PERIM_RAD * sin(theta)

            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = CIRCLE_RAD,
                x = x,
                y = y
                )
            
            material = self.material_gen(r = 1, g = 0, b = 1)
            self.circle_container.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container[i])

            # Collect events until released
            listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release
            )

            listener.start()

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
    
    def update_note_list(self, i, t_diff = 0):
            if i == 'a':
                i == 11
            else:
                i = int(i)
                
            theta = 2 * pi * i / CIRCLE_CNT
            x = abs(PERIM_RAD - t_diff) * cos(theta)
            y = abs(PERIM_RAD - t_diff) * sin(theta)

            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = CIRCLE_RAD - 0.5,
                x = x,
                y = y
                )
            
            material = self.material_gen(r = 0, g = 1, b = 0)
            self.circle_note_container[i - 1].append(Mesh(self.geometry, material))


    def update(self):

        cur_t = str(trunc(self.time*10)/10) 

        # clear out note circles:
        for i in self.circle_note_container:
            for j in i:
                self.scene.remove(j)
        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]

        # gather upcoming notes to be drawn:
        try:
            for j in current:
                self.update_note_list(j)
        except:
            pass
        
        # draw all notes
        for i in self.circle_note_container:
            for j in i:
                self.scene.add(j)

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

def on_press(key):
    if key in COMBINATION:
        current.add(key.char)
    
def on_release(key):
    try:
        current.remove(key.char)
    except KeyError:
        pass

if __name__ == '__main__':
    
    Thread(target = func1).start()
    Thread(target = func2).start()

# to share data between threads:
# https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

