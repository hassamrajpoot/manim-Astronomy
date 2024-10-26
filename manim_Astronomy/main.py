from manim import *
from vedo import Mesh
import numpy as np

from stellar_objects import HubbleSpaceTelescope

class Space(ThreeDScene):
    def construct(self):
        t = HubbleSpaceTelescope()
        self.add(t)
        self.wait(2)
