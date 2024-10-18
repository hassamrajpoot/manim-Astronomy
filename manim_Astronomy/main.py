from manim import *
from stellar_objects import Star, Planet

config.renderer = "opengl"

class Space(ThreeDScene):
    def construct(self):
        self.wait(5)
