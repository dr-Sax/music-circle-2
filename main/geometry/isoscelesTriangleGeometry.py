from geometry.geometry import Geometry
from math import sin, cos, pi
import numpy as np

class IsoscelesTriangleGeometry(Geometry):
    def __init__(self, base, height):
        super().__init__()

        positionData = []
        colorData = []
        uvData = []

        P1 = [-base / 2, - height / 2, 0]
        P2 = [0, height / 2, 0]
        P3 = [base / 2,  - height / 2, 0]
        positionData.append(P1)
        positionData.append(P2)
        positionData.append(P3)

        colorData.append([1, 1, 1])
        colorData.append([1, 0, 0])
        colorData.append([0, 0, 1])

        # texture coordinates
        T0, T1, T2 = [0, 0], [1 / 2, height / base], [1, 0]
        uvData = [T0, T1, T2, T0]
        
        self.addAttribute('vec3', 'vertexPosition', positionData)
        self.addAttribute('vec3', 'vertexColor', colorData)
        self.addAttribute('vec2', 'vertexUV', uvData)
        self.countVertices()