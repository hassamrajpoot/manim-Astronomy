=========================
Astronomy Plugin for Manim
=========================

.. image:: Logo.png
   :align: center

A Manim Extension for Creating Astronomical Visualizations
-----------------------------------------------------------

**Currently in Development**: This plugin is a work in progress. Features and functionality may change as we refine the project!

.. note::

   **Disclaimer**: This plugin is not a scientific simulation tool and may not depict accurate physics or astronomical phenomena. It is designed for **visualization purposes only**. For accurate astronomical simulations, consider using specialized tools!

Features
--------
- **Elliptical Orbits**: Visualize planetary orbits with elliptical paths.
- **Celestial Bodies**: Create and animate stars, planets, space telescopes, and more in a 3D space.
- **Solar System Models**: Build solar system representations.
- **Space-Time Grids**: Visualize the concept of spacetime curvature using space-time grids.

Installation
------------
Make sure you have `Manim` installed on your machine. Then, you can install this plugin by cloning the repository and installing the required dependencies.

.. code-block:: bash

   git clone https://github.com/hassamrajpoot/manim-Astronomy.git
   cd manim-Astronomy
   pip install -r requirements.txt

Usage
-----
Here's a quick example of how to use the plugin to create an animation of a planet orbiting a star:

.. code-block:: python

   from manim import *
   from manim_Astronomy.stellar_objects import Planet, Star

   config.renderer = "opengl"

   class KeplersSecondLaw(ThreeDScene):
       def construct(self):
           star = Star(radius=1, size_of_particle=0.001, colors=[YELLOW])
           self.add(star)
           planet = Planet(center=[1, 0, 0], radius=0.05)
           self.add(planet)
           a = 4
           b = 6
           orbit = ParametricFunction(
               lambda t: np.array([a * np.cos(t), b * np.sin(t), 0]),
               t_range=[0, TAU],
               color=BLUE
           )
           self.add(orbit)
           last_pos = [orbit.point_from_proportion(1)]

           def trace(mob):
               curr_pos = mob.get_center()
               self.add(Line3D(last_pos[0], curr_pos, color=BLUE))
               last_pos[0] = curr_pos

           time_tracker = ValueTracker(0)
           planet.add_updater(lambda mob: mob.move_to(orbit.point_from_proportion(time_tracker.get_value())))

           def get_swept_sector(start, end, close_factor=0.1):
               num_points = 50
               start = np.clip(start, 0, 1)
               end = np.clip(end, 0, 1)
               points = [orbit.point_from_proportion(start)]
               for alpha in np.linspace(start, end, num_points):
                   points.append(orbit.point_from_proportion(alpha))
               last_point = orbit.point_from_proportion(end)
               closing_point = last_point * close_factor
               points.append(closing_point)
               return Polygon(*points, fill_opacity=0.3, color=YELLOW)

           sweep_intervals = [(0.1, 0.2), (0.4, 0.5), (0.7, 0.8)]
           cumulative_sweep = VGroup()

           def update_swept_area():
               current_time = time_tracker.get_value()
               for start, end in sweep_intervals:
                   if start <= current_time <= end:
                       new_swept_area = get_swept_sector(start, current_time)
                       cumulative_sweep.add(new_swept_area)
               return cumulative_sweep

           sweep_area = always_redraw(lambda: update_swept_area())
           self.add(sweep_area)
           self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES)
           planet.add_updater(trace)
           self.play(time_tracker.animate.set_value(1), run_time=5, rate_func=linear)
           self.wait(5)

.. image:: displaygif.gif
   :align: center
   :alt: Rendered Scene

Main Components
---------------
- **Planet**: Create spherical objects representing planets.
- **Star**: Create a Star using particles.
- **SpaceTimeFabric**: A grid-like representation of space-time, often used to demonstrate the concept of gravitational curvature.

Contributing
------------
We welcome contributions! Please submit issues or pull requests to help improve the plugin. Make sure to follow our `contribution guidelines <https://docs.manim.community/en/stable/contributing.html>`_ for code style and testing. 🤝

License
-------
This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details. 📜

Credits
-------
Developed by `Hassam ul Haq <https://github.com/hassamrajpoot/>`. Special thanks to the `Manim Community <https://www.manim.community/>`_ for making this project possible! 🌟
