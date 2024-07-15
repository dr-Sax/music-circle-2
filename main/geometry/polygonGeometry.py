from geometry.geometry import Geometry
from math import sin, cos, pi
import numpy as np

class PolygonGeometry(Geometry):

    def __init__(self, sides = 3, radius = 1, x = 0, y = 0, theta1 = 0, theta2 = 2 * pi):
        super().__init__()

        A = 2 * pi / sides
        n1 = theta1 / (2 * pi) * sides
        n2 = theta2 / (2 * pi) * sides
        positionData = []
        colorData = []
        
        uvData = []
        uvCenter = [0.5, 0.5]

        for n in np.arange(n1, n2 + 1):
            #positionData.append([0, 0, 0])
            positionData.append([radius * cos(n * A) + x, radius * sin(n * A) + y, 0])
            positionData.append([radius * cos((n + 1) * A) + x, radius * sin((n + 1) * A) + y, 0])
            colorData.append([1, 1, 1])
            colorData.append([1, 0, 0])
            colorData.append([0, 0, 1])

            # texture:
            uvData.append(uvCenter)
            uvData.append(
                [
                    cos(n * A) * 0.5 + 0.5,
                    sin(n * A) * 0.5 + 0.5,
                ]
            )
            uvData.append(
                [
                    cos((n + 1) * A) * 0.5 + 0.5,
                    sin((n + 1) * A) * 0.5 + 0.5,
                ]
            )
        
        self.addAttribute('vec3', 'vertexPosition', positionData)
        self.addAttribute('vec3', 'vertexColor', colorData)
        self.addAttribute('vec2', 'vertexUV', uvData)
        self.countVertices()
