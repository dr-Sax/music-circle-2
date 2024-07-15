from math import pi, sin, cos
from numpy import linspace

class Circle():

    def __init__(self, theta_0, theta_f, radius, resolution, center_x = 0, center_y = 0):
        self.r = radius
        self.theta_0 = theta_0
        self.theta_f = theta_f
        self.num_points = resolution
        self.center_x = center_x
        self.center_y = center_y
    
    def circle_array(self):

        circle_points = []

        for theta in linspace(self.theta_0, self.theta_f, self.num_points):
            x = self.center_x + self.r * cos(theta)
            y = self.center_y + self.r * sin(theta)
            circle_points.append([x, y, 0.0])
            
        return circle_points
