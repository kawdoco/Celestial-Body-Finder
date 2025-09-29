# celestial_explorer_updated.py
import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pygame
import math

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
ORANGE = (255, 165, 0)
BROWN = (200, 150, 100)

# ---------------------- #
# Celestial Classes
# ---------------------- #
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
    def __init__(self, name, mass, gravity, radius, has_life=False):
        super().__init__(name, "Planet", mass, gravity, radius)
        self.has_life = has_life

    def get_info(self):
        return super().get_info() + f"Supports Life: {'Yes' if self.has_life else 'No'}\n"

class Moon(CelestialObject):
    def __init__(self, name, mass, gravity, radius, planet):
        super().__init__(name, "Moon", mass, gravity, radius)
        self.planet = planet

    def get_info(self):
        return super().get_info() + f"Orbits: {self.planet}\n"

class Star(CelestialObject):
    def __init__(self, name, mass, gravity, radius, temperature):
        super().__init__(name, "Star", mass, gravity, radius)
        self.temperature = temperature

    def get_info(self):
        return super().get_info() + f"Surface Temperature: {self.temperature} K\n"

# ---------------------- #
# Dataset
# ---------------------- #
DATASET = {
    "earth": Planet("Earth", 5.97e24, 9.8, 6371, has_life=True),
    "mars": Planet("Mars", 6.39e23, 3.7, 3389),
    "moon": Moon("Moon", 7.35e22, 1.62, 1737, "Earth"),
    "jupiter": Planet("Jupiter", 1.898e27, 24.8, 69911),
    "sun": Star("Sun", 1.989e30, 274, 696340, 5778),
}

# ---------------------- #
# Pygame Mini Solar System Classes
# ---------------------- #
class CelestialBody:
    def __init__(self, name, radius, color, orbit_distance, orbital_period, info_text):
        self.name = name
        self.radius = radius
        self.color = color
        self.orbit_distance = orbit_distance
        self.orbital_period = orbital_period
        self.info_text = info_text
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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))
        if self.is_highlighted:
            pygame.draw.circle(screen, LIGHT_GREEN, (int(self.x), int(self.y)), int(self.radius) + 3, 2)
        font = pygame.font.Font(None, 24)
        screen.blit(font.render(self.name, True, WHITE), (self.x + self.radius + 5, self.y - self.radius))

    def get_info(self):
        return self.info_text

# --- Solar System Data ---
PLANET_DATA = [
    CelestialBody("Sun", 30, YELLOW, 0, 0,
        "Name: Sun\nType: Star\nMass: 1.989e30 kg\nGravity: 274 m/s²\nRadius: 696,340 km\nTemp: 5778 K"),
    CelestialBody("Earth", 9, BLUE, 120, 365,
        "Name: Earth\nType: Planet\nMass: 5.97e24 kg\nGravity: 9.8 m/s²\nRadius: 6,371 km\nHas Life: Yes"),
    CelestialBody("Mars", 6, RED, 180, 687,
        "Name: Mars\nType: Planet\nMass: 6.39e23 kg\nGravity: 3.7 m/s²\nRadius: 3,389 km"),
    CelestialBody("Moon", 4, GRAY, 40, 27,
        "Name: Moon\nType: Moon\nMass: 7.35e22 kg\nGravity: 1.62 m/s²\nRadius: 1,737 km\nOrbits: Earth"),
    CelestialBody("Jupiter", 18, BROWN, 260, 4333,
        "Name: Jupiter\nType: Planet\nMass: 1.898e27 kg\nGravity: 24.8 m/s²\nRadius: 69,911 km")
]

SOLAR_SYSTEM = {body.name.lower(): body for body in PLANET_DATA}

# ---------------------- #
# Tkinter App
# ---------------------- #
class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Celestial Explorer Mini Solar System ✨")
        self.root.geometry("1200x780")
        self.root.configure(bg="#0b0f1a")

        # Title
        tk.Label(root, text="🌌 Celestial Body Finder",
                 font=("Helvetica", 26, "bold"), fg="#00e6ff", bg="#0b0f1a").pack(pady=10)

        # Top Buttons Frame
        button_frame = tk.Frame(root, bg="#0b0f1a")
        button_frame.pack(pady=5)
        for body_name in ["Earth", "Mars", "Moon", "Jupiter", "Sun"]:
            tk.Button(button_frame, text=body_name, font=("Arial", 12, "bold"),
                      bg="#00e6ff", fg="black", width=10,
                      command=lambda name=body_name.lower(): self.select_object(name)).pack(side="left", padx=5)

        # Content Frame
        content_frame = tk.Frame(root, bg="#0b0f1a")
        content_frame.pack(fill="both", expand=True, pady=6, padx=12)

        # Left Panel: Info
        left_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        left_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        tk.Label(left_frame, text="🌠 Object Information",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=8)
        self.result_text = scrolledtext.ScrolledText(left_frame, height=20, width=50,
                                                     wrap="word", font=("Consolas", 12),
                                                     bg="#0b0f1a", fg="white", insertbackground="white")
        self.result_text.pack(pady=6, padx=8)

        # Right Panel: Pygame Mini Solar System
        right_frame = tk.Frame(content_frame, bg="#0b0f1a", width=700, height=700)
        right_frame.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        right_frame.pack_propagate(False)
        self.pygame_frame = right_frame

        # Status bar
        self.status = tk.Label(root, text="Ready", anchor="w", bg="#0b0f1a", fg="white")
        self.status.pack(fill="x", side="bottom")

        # Initialize Pygame inside Tkinter Frame
        os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib' if sys.platform.startswith("win") else ''
        pygame.init()
        self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(),
                                               self.pygame_frame.winfo_height()))
        pygame.display.init()

        self.time_factor = 0.5
        self.root.after(50, self.update_pygame)

        # Default selection
        self.select_object("earth")

    def select_object(self, name):
        if name in SOLAR_SYSTEM:
            obj = SOLAR_SYSTEM[name]
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, obj.get_info())
            for body in PLANET_DATA:
                body.is_highlighted = (body == obj)
            self.status.config(text=f"Selected: {obj.name}")
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Object not found.")
            self.status.config(text="Object not found")

    def update_pygame(self):
        self.screen.fill(BLACK)
        center_x, center_y = self.screen.get_width() / 2, self.screen.get_height() / 2
        for body in PLANET_DATA:
            body.update_position(self.time_factor, center_x, center_y)
            body.draw(self.screen, center_x, center_y)
        pygame.display.flip()
        self.root.after(30, self.update_pygame)


# ---------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
