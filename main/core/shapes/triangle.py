from math import pi, sin, cos, sqrt
from numpy import linspace

class Triangle():

    def __init__(self, center_x, center_y, side_length):
        self.center_x = center_x
        self.center_y = center_y
        self.side_length = side_length
    
    def equilateral_triangle_array(self):

        triangle_points = [
            [float(self.center_x), float(self.center_y + self.side_length / sqrt(3)), 0.0],
            [float(self.center_x - self.side_length / 2), float(self.center_y - self.side_length / (2 * sqrt(3))), 0.0],
            [float(self.center_x + self.side_length / 2), float(self.center_y - self.side_length / (2 * sqrt(3))), 0.0]
        ]
            
        return triangle_points