import numpy as np
from manim import *
from stellar_objects import *
def wave_function(u, v, t):
    wavelength = 0.5
    amplitude = 0.2
    distance_from_center = np.sqrt(u**2 + v**2)
    return amplitude * np.sin(2 * np.pi * (distance_from_center - t) / wavelength)

class Space(ThreeDScene):
    def construct(self):
        merged_masses = Dot3D(point=[0, 0, 0], radius=0.15, color=BLACK)
        fabric = SpaceTimeFabric(
            u_range=(-2, 2),
            v_range=(-2, 2),
            resolution=(50, 50),
            t_range=(-2,2),
            scaling_factor=0.1,
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=-90 * DEGREES)
        self.add(fabric, merged_masses)
        self.wait(1)
        t_tracker = ValueTracker(0)

        def update_fabric(mob):
            t = t_tracker.get_value()

            mob.become(SpaceTimeFabric(
                u_range=(-2, 2),
                v_range=(-2, 2),
                resolution=(50, 50),
                scaling_factor=0.1,
                t_range=(-2,2),
                func=wave_function,
                func_args=(t,)
            ))
        fabric.add_updater(update_fabric)
        self.play(t_tracker.animate.increment_value(5), run_time=10, rate_func=linear)
        self.wait(2)
