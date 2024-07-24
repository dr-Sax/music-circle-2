from geometry.geometry import Geometry
from math import sin, cos, pi
import numpy as np

class ParallelogramGeometry(Geometry):
    def __init__(self, base, height):
        super().__init__()

        positionData = []
        colorData = []
        uvData = []

        span = base + height

        P0 = [-span / 2, -height / 2, 0]
        P1 = [-height / 2, height / 2, 0]
        P2 = [span / 2,  height / 2, 0]
        P3 = [height / 2, -height / 2, 0]
        positionData = [P0, P3, P1,  P1, P3, P2]

        C0 = [1, 1, 1]
        C1 = [1, 0, 0]
        C2 = [0, 0, 1]
        C3 = [0, 1, 0]
        colorData = [C0, C3, C1,  C1, C3, C2]

        # texture coordinates
        T0, T1, T2, T3 = [0, 0], [height / span, height / span], [span / span, height / span], [base / span, 0]
        uvData = [T0, T3, T1,  T1, T3, T2]
        
        self.addAttribute('vec3', 'vertexPosition', positionData)
        self.addAttribute('vec3', 'vertexColor', colorData)
        self.addAttribute('vec2', 'vertexUV', uvData)
        self.countVertices()