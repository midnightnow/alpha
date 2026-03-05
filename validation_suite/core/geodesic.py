import math
import numpy as np

class Triangle51213:
    def __init__(self):
        self.a = 5
        self.b = 12
        self.c = 13
        self.angle_alpha = math.degrees(math.atan(5/12)) # ~22.62
        self.angle_beta = math.degrees(math.atan(12/5))  # ~67.38

class Spiral171:
    def __init__(self, constants):
        self.r_squared = constants["SPIRAL_PETAL"]
        self.radius = math.sqrt(self.r_squared)
        self.tilt = constants["AXIAL_TILT"]

    def get_arc_length(self, theta):
        # Simplistic arc length for r^2 = 171 spiral
        return self.radius * theta
