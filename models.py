# models.py
class CelestialObject:
    def __init__(self, name, object_type, mass, gravity, radius):
        self.name = name
        self.object_type = object_type
        self.mass = mass
        self.gravity = gravity
        self.radius = radius

    def get_info(self):
        return (f"Name: {self.name}\n"
                f"Type: {self.object_type}\n"
                f"Mass: {self.mass:.2e} kg\n"
                f"Gravity: {self.gravity} m/s²\n"
                f"Radius: {self.radius} km\n")

class Planet(CelestialObject):
    def __init__(self, name, mass, gravity, radius, has_life=False, moons=0, description=""):
        super().__init__(name, "Planet", mass, gravity, radius)
        self.has_life = has_life
        self.moons = moons
        self.description = description

    def get_info(self):
        info = super().get_info()
        info += f"Supports Life: {'Yes' if self.has_life else 'No'}\n"
        info += f"Number of Moons: {self.moons}\n"
        if self.description:
            info += f"\nDescription: {self.description}\n"
        return info

class Moon(CelestialObject):
    def __init__(self, name, mass, gravity, radius, planet, description=""):
        super().__init__(name, "Moon", mass, gravity, radius)
        self.planet = planet
        self.description = description

    def get_info(self):
        info = super().get_info()
        info += f"Orbits: {self.planet}\n"
        if self.description:
            info += f"\nDescription: {self.description}\n"
        return info

class Star(CelestialObject):
    def __init__(self, name, mass, gravity, radius, temperature, description=""):
        super().__init__(name, "Star", mass, gravity, radius)
        self.temperature = temperature
        self.description = description

    def get_info(self):
        info = super().get_info()
        info += f"Surface Temperature: {self.temperature} K\n"
        if self.description:
            info += f"\nDescription: {self.description}\n"
        return info