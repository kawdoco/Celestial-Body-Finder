# data_store.py
from models import Planet, Moon, Star

DATASET = {
    "earth": Planet("Earth", 5.97e24, 9.8, 6371, has_life=True, moons=1,
                   description="The only known planet to support life. Has diverse ecosystems and liquid water."),
    "mars": Planet("Mars", 6.39e23, 3.7, 3389, moons=2,
                  description="The 'Red Planet' with the largest volcano in the solar system - Olympus Mons."),
    "moon": Moon("Moon", 7.35e22, 1.62, 1737, "Earth",
                description="Earth's only natural satellite. The only celestial body visited by humans."),
    "jupiter": Planet("Jupiter", 1.898e27, 24.8, 69911, moons=95,
                     description="The largest planet in our solar system. A gas giant with a famous Great Red Spot."),
    "saturn": Planet("Saturn", 5.683e26, 10.4, 58232, moons=146,
                    description="Known for its spectacular ring system made of ice and rock particles."),
    "venus": Planet("Venus", 4.867e24, 8.87, 6052, moons=0,
                   description="The hottest planet with a thick, toxic atmosphere. Often called Earth's 'sister planet'."),
    "mercury": Planet("Mercury", 3.301e23, 3.7, 2440, moons=0,
                     description="The smallest and innermost planet. Has extreme temperature variations."),
    "sun": Star("Sun", 1.989e30, 274, 696340, 5778,
               description="The star at the center of our solar system. Provides energy for life on Earth."),
}