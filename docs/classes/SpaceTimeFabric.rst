SpaceTimeFabric Class
=====================

The `SpaceTimeFabric` class is designed to visualize the effects of gravitational fields on a space-time fabric. This class can be used in various scenarios to illustrate gravitational interactions and distortions caused by massive objects.

Overview
--------

The `SpaceTimeFabric` class takes parameters to define the ranges and resolution of the fabric, allowing for dynamic visualizations of gravitational effects in a 3D environment.

Parameters
----------

- **u_range** (`tuple`): Specifies the range of the u-axis.
- **v_range** (`tuple`): Specifies the range of the v-axis.
- **resolution** (`tuple`): Defines the resolution of the grid used to create the fabric.
- **t_range** (`tuple`): Specifies the range of time values for the animation.
- **scaling_factor** (`float`): Scales the visual representation of the fabric.
- **func** (`function`): Function to compute the gravitational potential based on object positions.
- **func_args** (`tuple`): Additional arguments to be passed to the `func` function.

Examples
--------

Illustration of Space-Time Fabric Distortion by a Star
------------------------------------------------------
This example demonstrates how the presence of massive objects, like stars, distorts the space-time fabric.

.. code-block:: python

    from manim import *
    import numpy as np
    from manim_Astronomy.stellar_objects import *

    def gravitational_potential(u, v, mass_positions, masses):
        G = 1 
        potential = 0
        epsilon = 0.1  
        for i in range(len(mass_positions)):
            mass_posu, mass_posv, mass_posz = mass_positions[i]
            M = masses[i]
            r = np.sqrt((u - mass_posu)**2 + (v - mass_posv)**2 + mass_posz**2)
            if r < epsilon:
                r += 0.05
            potential += -G * M / r 
        return potential

    class SpaceTimeFabricDistortionByAStar(ThreeDScene):
        def construct(self): 
            mass1 = Dot3D(point=[0, 0, 0.3], radius=0.3)
            mass2 = Dot3D(point=[1.1, 0, 0], radius=0.05)
            fabric = SpaceTimeFabric(
                u_range=(-2, 2),
                v_range=(-2, 2),
                resolution=(50, 50),
                t_range=(-2, 2)
            )
            self.add(fabric)
            self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES)
            self.wait(3)

            def fabric_updater(mob):
                mob.become(SpaceTimeFabric(
                    u_range=(-2, 2),
                    v_range=(-2, 2),
                    resolution=(50, 50),
                    t_range=(-2, 2),
                    scaling_factor=0.01,
                    func=gravitational_potential,
                    func_args=([mass1.get_center(), mass2.get_center()], [50, 2])
                ))
            fabric.add_updater(fabric_updater)
            self.play(FadeIn(mass1, mass2))
            self.wait(3)
            self.wait(10)
            
.. raw:: html

   <video width="600" height="400" controls autoplay loop>
       <source src="rendered_videos/SpaceTimeFabricDistortionByAStar.mp4" type="video/mp4">
       Your browser does not support the video tag.
   </video>
