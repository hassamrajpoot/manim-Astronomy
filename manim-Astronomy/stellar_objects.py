from manim import *
from manim.typing import Point3D
import numpy as np
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from astroquery.jplhorizons import Horizons
from astropy import units as u
import scipy
import scipy.integrate

class Star(ThreeDVMobject,metaclass=ConvertToOpenGL):
    SOLAR_PROPERTIES = {
        "radius": 696340,  
        "luminosity": 1,
        "temperature": 5800,
        "mass": 1
    }

    STARS_PROPERTIES = {
        "O": {"temperature": 40000, "luminosity": 1000000, "color": BLUE, "mass": 16, "radius": 1000000},
        "B": {"temperature": 20000, "luminosity": 25000, "color": BLUE_E, "mass": 2.1, "radius": 100000},
        "A": {"temperature": 8500, "luminosity": 80, "color": WHITE, "mass": 1.4, "radius": 150000},
        "F": {"temperature": 6500, "luminosity": 6, "color": YELLOW, "mass": 1.3, "radius": 120000},
        "G": {"temperature": 5800, "luminosity": 1, "color": YELLOW, "mass": 1, "radius": 696340},  
        "K": {"temperature": 4500, "luminosity": 0.4, "color": ORANGE, "mass": 0.8, "radius": 70000},
        "M": {"temperature": 3200, "luminosity": 0.04, "color": RED, "mass": 0.3, "radius": 70000}
    }

    MIN_LUMINOSITY = 0.01
    MIN_RADIUS = 1

    def __init__(
        self,
        center: Point3D = ORIGIN,
        radius: float = None,  
        star_type: str = "G",
        num_of_particles: int = 1000,
        size_of_particle: float = 0.00001,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        
        if radius is not None and radius <= 0:
            raise ValueError(f"Invalid radius '{radius}'. Radius must be a positive value.")
        if star_type not in self.STARS_PROPERTIES:
            raise ValueError(f"Invalid star type '{star_type}'. Supported types: {list(self.STARS_PROPERTIES.keys())}.")
        if size_of_particle <= 0:
            raise ValueError(f"Invalid particle size '{size_of_particle}'. Size must be a positive value.")

        self.star_type = star_type
        self.num_of_particles = num_of_particles
        self.size_of_particle = size_of_particle
        if radius is not None:
            self.radius = radius
        else:
            self.radius = self.STARS_PROPERTIES[self.star_type]["radius"]

        self.__set_star_properties()
        self.__set_star_scaled_properties()
        self.__setup_star_using_particles()
        self.shift(center)

    def __set_star_properties(self):
        star_properties = self.STARS_PROPERTIES[self.star_type]
        self.temperature = star_properties["temperature"] / self.SOLAR_PROPERTIES["temperature"]
        self.luminosity = star_properties["luminosity"] / self.SOLAR_PROPERTIES["luminosity"]
        self.color = star_properties["color"]
        self.mass = star_properties["mass"] / self.SOLAR_PROPERTIES["mass"]

    def __set_star_scaled_properties(self):
        if hasattr(self, 'radius'):
            self.__scaled_radius = self.radius / self.SOLAR_PROPERTIES["radius"]
        else:
            self.__scaled_radius = self.STARS_PROPERTIES[self.star_type]["radius"] / self.SOLAR_PROPERTIES["radius"]
        
        self.__scaled_luminosity = np.log10(max(self.luminosity, self.MIN_LUMINOSITY)) / np.log10(self.STARS_PROPERTIES["O"]["luminosity"])

    def __setup_star_using_particles(self):
        theta = np.random.uniform(0, 2 * np.pi, self.num_of_particles)
        cos_phi = np.random.uniform(-1, 1, self.num_of_particles)
        phi = np.arccos(cos_phi)
        x = self.__scaled_radius * np.sin(phi) * np.cos(theta)
        y = self.__scaled_radius * np.sin(phi) * np.sin(theta)
        z = self.__scaled_radius * np.cos(phi)
        points = np.vstack([x, y, z]).T
        dots = [Dot(point=point, radius=self.size_of_particle, color= self.STARS_PROPERTIES[self.star_type]["color"], fill_opacity=self.STARS_PROPERTIES[self.star_type]["luminosity"]) for point in points]
        sphere = VGroup(*dots)
        self.add(sphere)
    def get_star_properties(self):
        return {
                "star_type": self.star_type,
                "radius" : self.radius,
                "temperature": self.temperature,
                "luminosity":self.luminosity,
                "color": self.color,
                "mass" : self.mass
        }
    

class Planet(ThreeDVMobject, metaclass=ConvertToOpenGL):
    PLANETS = {
        'Earth': 399,     
        'Mars': 499,     
        'Mercury': 199,   
        'Venus': 299,     
        'Saturn': 699,    
        'Neptune': 899,   
        'Uranus': 799,    
        'Jupiter': 599   
    }

    def __init__(
        self,
        center=ORIGIN,
        radius=0.05,  
        planet_name='Earth',
        initial_conditions=None,
        mass=5.972e24,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        
        if planet_name not in self.PLANETS:
            raise ValueError(f"Planet '{planet_name}' not found. Available planets: {list(self.PLANETS.keys())}")
        
        self.planet_name = planet_name
        self.center = center
        self.radius = radius
        if initial_conditions is None:
            initial_conditions = self.get_initial_conditions(self.planet_name)
        self.position = initial_conditions["position"]
        self.velocity = initial_conditions["velocity"]
        self.mass = mass if mass is not None and mass != 0 else 1.0
        self.planet_sphere = Dot3D(radius=self.radius, **kwargs).move_to(self.position)
        self.add(self.planet_sphere)

    def get_initial_conditions(self, planet_name):
        planet_id = self.PLANETS[planet_name]
        obj = Horizons(id=planet_id, location='@sun', epochs=2000.0)
        eph = obj.vectors()
        position = np.array([eph['x'][0], eph['y'][0], eph['z'][0]]) * 1.496e11
        velocity = np.array([eph['vx'][0], eph['vy'][0], eph['vz'][0]])  * (1.496e11/86400)  
        scale_factor_position = 1  
        scale_factor_velocity = 1  
        return {
            "position": np.array(position) / scale_factor_position,
            "velocity": np.array(velocity) / scale_factor_velocity
        }

    def compute_orbit(self, central_mass=1.989e30, dt=100000, total_time=31536000):
        initial_conditions_data = self.get_initial_conditions(self.planet_name)
        initial_conditions = [
            initial_conditions_data['position'][0], initial_conditions_data['velocity'][0],
            initial_conditions_data['position'][1], initial_conditions_data['velocity'][1],
            initial_conditions_data['position'][2], initial_conditions_data['velocity'][2]
                            ]

        def f(t, state):
            x, vx, y, vy, z, vz = state
            r = np.sqrt(x**2 + y**2 + z**2) + 1e-5  
            G = 6.67430e-11
            Fx = -G * central_mass * self.mass * x / r**3
            Fy = -G * central_mass * self.mass * y / r**3
            Fz = -G * central_mass * self.mass * z / r**3
            return [vx, Fx / self.mass, vy, Fy / self.mass, vz, Fz / self.mass]


        t_span = (0, total_time)
        t_eval = np.arange(0, total_time, dt)  
        sol = scipy.integrate.solve_ivp(
        f, 
        t_span, 
        initial_conditions, 
        t_eval=t_eval, 
        rtol=1e-3, 
        atol=1e-6,
        method='DOP853')
        x = sol.y[0] / 1e12
        y = sol.y[2] / 1e12
        z = sol.y[4] / 1e12
        positions = np.column_stack((x, y, z))
        return positions



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
