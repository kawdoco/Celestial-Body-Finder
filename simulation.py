# simulation.py
import math
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
ORANGE = (255, 165, 0)
BROWN = (200, 150, 100)
LIGHT_BROWN = (210, 180, 140)

class CelestialBody:
    def __init__(self, name, radius, color, orbit_distance, orbital_period, info_text, has_rings=False):
        self.name = name
        self.radius = radius
        self.color = color
        self.orbit_distance = orbit_distance
        self.orbital_period = orbital_period
        self.info_text = info_text
        self.has_rings = has_rings
        self.angle = 0
        self.x = 0
        self.y = 0
        self.is_highlighted = False

    def update_position(self, time_factor, center_x, center_y):
        if self.orbital_period != 0:
            self.angle += (2 * math.pi / self.orbital_period) * time_factor
        self.x = center_x + self.orbit_distance * math.cos(self.angle)
        self.y = center_y + self.orbit_distance * math.sin(self.angle)

    def draw(self, screen, center_x, center_y):
        if self.orbit_distance > 0:
            pygame.draw.circle(screen, GRAY, (int(center_x), int(center_y)), int(self.orbit_distance), 1)

        if self.has_rings and self.name == "Saturn":
            ring_radius1 = self.radius * 1.8
            ring_radius2 = self.radius * 2.2
            pygame.draw.circle(screen, LIGHT_BROWN, (int(self.x), int(self.y)), int(ring_radius2), 2)
            pygame.draw.circle(screen, LIGHT_BROWN, (int(self.x), int(self.y)), int(ring_radius1), 2)

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

        if self.is_highlighted:
            pygame.draw.circle(screen, LIGHT_GREEN, (int(self.x), int(self.y)), int(self.radius) + 3, 2)

        font = pygame.font.Font(None, 24)
        screen.blit(font.render(self.name, True, WHITE), (self.x + self.radius + 5, self.y - self.radius))

    def get_info(self):
        return self.info_text

    def is_clicked(self, pos):
        distance = math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)
        return distance <= self.radius

PLANET_DATA = [
    CelestialBody("Sun", 30, YELLOW, 0, 0,
        "Name: Sun\nType: Star\nMass: 1.989e30 kg\nGravity: 274 m/s²\nRadius: 696,340 km\nTemp: 5778 K\n\nDescription: The star at the center of our solar system. Provides energy for life on Earth."),
    CelestialBody("Mercury", 5, BROWN, 60, 88,
        "Name: Mercury\nType: Planet\nMass: 3.301e23 kg\nGravity: 3.7 m/s²\nRadius: 2,440 km\nMoons: 0\n\nDescription: The smallest and innermost planet. Has extreme temperature variations."),
    CelestialBody("Venus", 8, ORANGE, 90, 225,
        "Name: Venus\nType: Planet\nMass: 4.867e24 kg\nGravity: 8.87 m/s²\nRadius: 6,052 km\nMoons: 0\n\nDescription: The hottest planet with a thick, toxic atmosphere. Often called Earth's 'sister planet'."),
    CelestialBody("Earth", 9, BLUE, 120, 365,
        "Name: Earth\nType: Planet\nMass: 5.97e24 kg\nGravity: 9.8 m/s²\nRadius: 6,371 km\nHas Life: Yes\nMoons: 1\n\nDescription: The only known planet to support life. Has diverse ecosystems and liquid water."),
    CelestialBody("Moon", 3, GRAY, 20, 27,
        "Name: Moon\nType: Moon\nMass: 7.35e22 kg\nGravity: 1.62 m/s²\nRadius: 1,737 km\nOrbits: Earth\n\nDescription: Earth's only natural satellite. The only celestial body visited by humans."),
    CelestialBody("Mars", 6, RED, 160, 687,
        "Name: Mars\nType: Planet\nMass: 6.39e23 kg\nGravity: 3.7 m/s²\nRadius: 3,389 km\nMoons: 2\n\nDescription: The 'Red Planet' with the largest volcano in the solar system - Olympus Mons."),
    CelestialBody("Jupiter", 18, BROWN, 220, 4333,
        "Name: Jupiter\nType: Planet\nMass: 1.898e27 kg\nGravity: 24.8 m/s²\nRadius: 69,911 km\nMoons: 95\n\nDescription: The largest planet in our solar system. A gas giant with a famous Great Red Spot."),
    CelestialBody("Saturn", 16, LIGHT_BROWN, 280, 10759, True,
        "Name: Saturn\nType: Planet\nMass: 5.683e26 kg\nGravity: 10.4 m/s²\nRadius: 58,232 km\nMoons: 146\n\nDescription: Known for its spectacular ring system made of ice and rock particles."),
]

SOLAR_SYSTEM = {body.name.lower(): body for body in PLANET_DATA}
