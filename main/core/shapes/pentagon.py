from math import pi, sin, cos, sqrt

class Pentagon():

    def __init__(self, center_x = 0, center_y = 0, circ_radius = 1):
        self.center_x = center_x
        self.center_y = center_y
        self.circ_radius = circ_radius
    
    def pentagram_coords(self):

        c1 = cos(2 * pi / 5)
        c2 = cos(pi / 5)
        s1 = sin(2 * pi / 5)
        s2 = sin(4 * pi / 5)
        
        p1 = [0.0, 1.0, 0.0]
        p2 = [s1, c1, 0.0]
        p3 = [s2, -c2, 0.0]
        p4 = [-s2, -c2, 0.0]
        p5 = [-s1, c1, 0.0]

        return [p1, p2, p3, p4, p5]
    
    def diamond_coords(self):
        c1 = cos(2 * pi / 5)
        c2 = cos(pi / 5)
        s1 = sin(2 * pi / 5)
        s2 = sin(4 * pi / 5)
        
        p1 = [0.0, -1.0, 0.0]
        p2 = [s1, c1, 0.0]
        p3 = [s2, c2, 0.0]
        p4 = [-s2, c2, 0.0]
        p5 = [-s1, c1, 0.0]

        return [p1, p2, p3, p4, p5]
    
    def inverted_pentagon_coords(self):
        c1 = cos(2 * pi / 5)
        c2 = cos(pi / 5)
        s1 = sin(2 * pi / 5)
        s2 = sin(4 * pi / 5)
        
        p1 = [0.0, -1.0, 0.0]
        p2 = [-s1, -c1, 0.0]
        p3 = [-s2, c2, 0.0]
        p4 = [s2, c2, 0.0]
        p5 = [s1, -c1, 0.0]

        return [p1, p5, p3, p4, p2]