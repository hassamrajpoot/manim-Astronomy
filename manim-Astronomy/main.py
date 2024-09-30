from manim import *
from sympy import Plane
from stellar_objects import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class Space(ThreeDScene):
    def construct(self):
        orbit1 = ThreeDVMobject().set_points_as_corners(Planet().compute_orbit())
        self.add(orbit1.scale([2,0.5,1]))
        orbit2 = ThreeDVMobject().set_points_as_corners(Planet(planet_name='Mars',mass=6.39e+23).compute_orbit(total_time=59354880))
        self.add(orbit2.scale([2,0.5,1]))
        orbit3 = ThreeDVMobject().set_points_as_corners(Planet(planet_name='Jupiter',mass=1.898e+27).compute_orbit(total_time=374335760))
        self.add(orbit3.scale([2,0.5,1]))
        self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES)
        self.wait(3)
