from manim import *
from manim.typing import Point3D
import numpy as np
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL



class Star(ThreeDVMobject, metaclass=ConvertToOpenGL):
    def __init__(
        self,
        center: Point3D = ORIGIN,
        radius: float = 0.5,
        num_of_particles: int = 1000,
        size_of_particle: float = 0.000001,
        colors: list = [YELLOW],      
        luminosity: float = 1.0,      
        mass: float = 1.0,           
        temperature: float = 6000,    
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        
        self.center = center
        self.radius = radius
        self.num_of_particles = num_of_particles
        self.size_of_particle = size_of_particle
        self.colors = colors
        self.luminosity = luminosity
        self.mass = mass
        self.temperature = temperature
        
        
        self.__setup_star_using_particles()
        self.shift(self.center)

    def __setup_star_using_particles(self):
       
        theta = np.random.uniform(0, 2 * np.pi, self.num_of_particles)
        cos_phi = np.random.uniform(-1, 1, self.num_of_particles)
        phi = np.arccos(cos_phi)

        
        x = self.radius * np.sin(phi) * np.cos(theta)
        y = self.radius * np.sin(phi) * np.sin(theta)
        z = self.radius * np.cos(phi)

       
        points = np.vstack([x, y, z]).T

        
        dots = [
            Dot3D(point=point, radius=self.size_of_particle, color=np.random.choice(self.colors), fill_opacity=self.luminosity) 
            for point in points
        ]
        self.star = VGroup(*dots)
        self.add(self.star)
    
    
class Planet(ThreeDVMobject, metaclass=ConvertToOpenGL):
    def __init__(
        self,
        center=ORIGIN,
        radius=0.05, 
        include_planetary_disc=False,  
        ring_inner_radius=0.1,  
        ring_outer_radius=0.15,  
        num_particles=100,
        size_of_particle = 0.01,  
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.center = center
        self.radius = radius
        self.planet_sphere = Dot3D(radius=self.radius, **kwargs).move_to(self.center)
        self.add(self.planet_sphere)
        if include_planetary_disc:
            self.ring_inner_radius = ring_inner_radius
            self.ring_outer_radius = ring_outer_radius
            self.num_particles = num_particles
            self.size_of_particle = size_of_particle
            self.__setup_planetary_disc_using_particles()
        else:
            self.planetary_disc = VGroup()  
        self.planet = VGroup(self.planet_sphere, self.planetary_disc)
        self.add(self.planet)  
        self.planet.shift(self.center)

    def __setup_planetary_disc_using_particles(self):
        disc = VGroup()
        for _ in range(self.num_particles):
            angle = np.random.uniform(0, TAU)  
            radius = np.random.uniform(self.ring_inner_radius, self.ring_outer_radius)  
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            particle = Dot(radius=self.size_of_particle, color=WHITE).move_to(self.center + np.array([x, y, 0]))
            disc.add(particle)
        self.planetary_disc = disc
    





class SpaceTimeFabric(ThreeDVMobject, metaclass=ConvertToOpenGL):
    def __init__(
        self,
        func=None,              
        func_args=(),           
        u_range=(-1, 1),
        v_range=(-1, 1),
        resolution=(50, 50),
        scaling_factor=0.1,
        t_range=(-1, 1),
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.func = func if func is not None else (lambda u, v: 0)  
        self.func_args = func_args                                   
        self.u_range = u_range
        self.v_range = v_range
        self.resolution = resolution
        self.scaling_factor = scaling_factor
        self.t_range = t_range
        self.__generate_curves()

    def __generate_curves(self):
        u_values = np.linspace(self.u_range[0], self.u_range[1], self.resolution[0])
        v_values = np.linspace(self.v_range[0], self.v_range[1], self.resolution[1])
        wireframe_curves = VGroup()

        for u in u_values:
            curve = ParametricFunction(
                lambda v, u=u: np.array([
                    u, 
                    v, 
                    self.scaling_factor * self.func(u, v, *self.func_args)  
                ]),  
                color=self.stroke_color,
                stroke_width=self.stroke_opacity,
                t_range=self.t_range
            )
            wireframe_curves.add(curve)

        for v in v_values:
            curve = ParametricFunction(
                lambda u, v=v: np.array([
                    u, 
                    v, 
                    self.scaling_factor * self.func(u, v, *self.func_args)  
                ]),  
                color=self.stroke_color,
                stroke_width=self.stroke_opacity,
                t_range=self.t_range
            )
            wireframe_curves.add(curve)

        self.add(wireframe_curves)
        self.wireframe_curves = wireframe_curves

    def get_wireframe_curves(self):
        return self.wireframe_curves
