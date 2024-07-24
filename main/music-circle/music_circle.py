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

WIDTH = 2560 / 2
HEIGHT = 1400 / 2
Z = 20  # Sets camera distance away from xy plane
CIRCLE_CNT = 12
CIRCLE_RAD = 1
PERIM_RAD = 10

sequence = {'0.1': [1, 1], '0.5': [1, 1], '1.0': [8, 5], '1.5': [8, 1], '2.0': [10, 6], '2.4': [10], '2.9': [8, 5], '3.4': [8, 1], '3.9': [6, 3], '4.4': [6, 12], '4.9': [5, 1], '5.4': [5, 10], '5.8': [3], '6.1': [5], '6.2': [3], '6.3': [5, 3, 8], '6.7': [5], '7.0': [1, 1], '8.0': [1, 1], '8.5': [1, 1], '9.0': [8, 5], '9.4': [8], '9.9': [10], '10.4': [10, 1], '10.9': [8, 5], '11.4': [8, 1], '11.8': [6, 3], '12.3': [6, 12], '12.8': [5, 1], '13.3': [5, 10], '13.8': [3, 6], '14.1': [5], '14.2': [3, 5, 8], '14.3': [3], '14.7': [5], '14.9': [1, 1], '16.0': [8, 5], '16.4': [8, 8], '16.9': [6, 3], '17.3': [6], '17.8': [5, 1], '18.2': [5], '18.7': [3, 12], '19.2': [3, 8], '19.7': [8, 5], '20.2': [8, 8], '20.7': [6, 3], '21.2': [6, 8], '21.7': [5, 1], '22.0': [6], '22.1': [5, 1], '22.2': [6, 5], '22.6': [6, 3], '22.8': [5, 1, 8], '23.5': [3, 12], '24.1': [1, 1], '24.6': [1, 1], '25.0': [8], '25.5': [8, 1], '26.0': [10, 6], '26.5': [10, 1], '27.0': [8, 5], '27.5': [8, 1], '28.0': [6, 3], '28.4': [6], '28.9': [5], '29.5': [5, 10], '30.0': [3, 6], '30.3': [5, 3], '30.4': [5, 8], '30.5': [3], '30.9': [5], '31.1': [1, 1], '32.2': [8, 5], '32.7': [8, 8], '33.1': [6, 3], '33.6': [6, 8], '34.1': [5, 1], '34.5': [5, 8], '35.0': [3, 12], '35.5': [3, 8], '36.0': [8, 5], '36.5': [8, 8], '36.9': [6], '37.5': [6, 8], '38.0': [5, 1], '38.3': [6], '38.4': [5, 6, 1], '38.5': [5], '39.0': [6, 3], '39.1': [5], '39.9': [3, 12], '40.6': [1, 1], '41.1': [1, 1], '41.6': [8, 5], '42.0': [8], '42.5': [10], '43.0': [10], '43.5': [8, 5], '44.0': [8, 1], '44.4': [6, 3], '44.9': [6], '45.4': [5, 1], '45.9': [5, 10], '46.4': [3], '46.7': [5], '46.8': [3], '46.9': [5, 8], '47.0': [3], '47.4': [5], '47.6': [1], '2.5': [1], '5.9': [6], '9.5': [1], '10.0': [6], '17.4': [8], '18.3': [8], '25.1': [5], '28.5': [12], '29.0': [1], '37.0': [3], '39.2': [1, 8], '42.1': [1], '42.6': [6], '43.1': [1], '45.0': [12], '46.5': [6], '47.7': [1]}
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
    
    def update_note_list(self, i, t_diff):
            theta = 2 * pi * i / CIRCLE_CNT
            x = abs(PERIM_RAD - t_diff) * cos(theta)
            y = abs(PERIM_RAD - t_diff) * sin(theta)

            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = CIRCLE_RAD - 0.5,
                x = x,
                y = y
                )
            
            material = self.material_gen(r = 0, g = 0, b = 1)
            self.circle_note_container[i - 1].append(Mesh(self.geometry, material))

    # assumes sequence is in order
    def get_upcoming_notes(self, cur_time, sequence):
        res = [[round(abs(float(tstamp) - float(cur_time)), 2), notes_list] for tstamp, notes_list in sequence.items() if (float(tstamp) - float(cur_time) < 2) and (float(tstamp) - float(cur_time) > 0)]
        return res

    def update(self):

        cur_t = str(trunc(self.time*10)/10) 

        # clear out note circles:
        for i in self.circle_note_container:
            for j in i:
                self.scene.remove(j)
        self.circle_note_container = [[], [], [], [], [], [], [], [], [], [], [], []]

        # gather upcoming notes to be drawn:
        note_queue = self.get_upcoming_notes(cur_time = cur_t, sequence = sequence)
        for note_stamp in note_queue:
            t_dif = note_stamp[0]
            for note in note_stamp[1]:
                self.update_note_list(int(note), t_dif * 8)
        
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

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()

# to share data between threads:
# https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

