# celestial_explorer_enhanced.py
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
DARK_BLUE = (0, 0, 139)
PURPLE = (128, 0, 128)
LIGHT_BROWN = (210, 180, 140)
DARK_RED = (139, 0, 0)

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

# ---------------------- #
# Dataset
# ---------------------- #
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

# ---------------------- #
# Pygame Mini Solar System Classes
# ---------------------- #
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
        # Draw orbit path
        if self.orbit_distance > 0:
            pygame.draw.circle(screen, GRAY, (int(center_x), int(center_y)), int(self.orbit_distance), 1)
        
        # Draw rings for Saturn
        if self.has_rings and self.name == "Saturn":
            ring_radius1 = self.radius * 1.8
            ring_radius2 = self.radius * 2.2
            pygame.draw.circle(screen, LIGHT_BROWN, (int(self.x), int(self.y)), int(ring_radius2), 2)
            pygame.draw.circle(screen, LIGHT_BROWN, (int(self.x), int(self.y)), int(ring_radius1), 2)
        
        # Draw the celestial body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))
        
        # Draw highlight if selected
        if self.is_highlighted:
            pygame.draw.circle(screen, LIGHT_GREEN, (int(self.x), int(self.y)), int(self.radius) + 3, 2)
        
        # Draw name label
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.name, True, WHITE)
        screen.blit(text_surface, (self.x + self.radius + 5, self.y - self.radius))

    def get_info(self):
        return self.info_text

    def is_clicked(self, pos):
        distance = math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)
        return distance <= self.radius

# --- Solar System Data ---
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

# ---------------------- #
# Tkinter App
# ---------------------- #
class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Celestial Explorer - Interactive Solar System ✨")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0b0f1a")
        
        # Initialize simulation state
        self.time_factor = 0.5
        self.is_paused = False
        self.pygame_initialized = False
        
        self.setup_ui()
        self.init_pygame()
        
        # Default selection
        self.select_object("earth")

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#0b0f1a")
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="🌌 Celestial Explorer", 
                 font=("Helvetica", 28, "bold"), fg="#00e6ff", bg="#0b0f1a").pack()
        tk.Label(title_frame, text="Interactive Solar System Simulator", 
                 font=("Helvetica", 14), fg="#ffffff", bg="#0b0f1a").pack()

        # Search Frame
        self.create_search_frame()

        # Quick Access Buttons Frame
        self.create_quick_access_buttons()

        # Control Panel
        self.create_control_panel()

        # Content Frame
        content_frame = tk.Frame(self.root, bg="#0b0f1a")
        content_frame.pack(fill="both", expand=True, pady=10, padx=15)

        # Left Panel: Information
        self.create_info_panel(content_frame)

        # Right Panel: Pygame Simulation
        self.create_simulation_panel(content_frame)

        # Status Bar
        self.create_status_bar()

    def create_search_frame(self):
        search_frame = tk.Frame(self.root, bg="#0b0f1a")
        search_frame.pack(pady=8)
        
        tk.Label(search_frame, text="Search Celestial Body:", 
                font=("Arial", 12, "bold"), fg="white", bg="#0b0f1a").pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=("Arial", 12), width=25, bg="#1c2230", fg="white", 
                               insertbackground="white")
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", self.on_search)
        
        tk.Button(search_frame, text="Search", font=("Arial", 10, "bold"),
                  command=self.on_search, bg="#00e6ff", fg="black", width=8).pack(side="left", padx=5)

    def create_quick_access_buttons(self):
        button_frame = tk.Frame(self.root, bg="#0b0f1a")
        button_frame.pack(pady=8)
        
        celestial_bodies = ["Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn"]
        colors = ["#ffcc00", "#8b7355", "#ffa500", "#1e90ff", "#a9a9a9", "#ff4500", "#cd853f", "#f4a460"]
        
        for i, body in enumerate(celestial_bodies):
            tk.Button(button_frame, text=body, font=("Arial", 10, "bold"),
                      bg=colors[i], fg="black" if body in ["Sun", "Venus"] else "white",
                      width=9, height=1,
                      command=lambda name=body.lower(): self.select_object(name)).pack(side="left", padx=3)

    def create_control_panel(self):
        control_frame = tk.Frame(self.root, bg="#1c2230", relief="ridge", bd=2)
        control_frame.pack(pady=8, padx=15, fill="x")
        
        # Time Control
        time_frame = tk.Frame(control_frame, bg="#1c2230")
        time_frame.pack(side="left", padx=20)
        
        tk.Label(time_frame, text="Time Speed:", font=("Arial", 11, "bold"),
                fg="white", bg="#1c2230").pack(side="left")
        
        self.time_scale = tk.Scale(time_frame, from_=0, to=2, resolution=0.1,
                                  orient="horizontal", command=self.set_time_factor,
                                  length=200, showvalue=True, 
                                  bg="#1c2230", fg="white", highlightbackground="#1c2230",
                                  troughcolor="#0b0f1a", sliderrelief="raised")
        self.time_scale.set(0.5)
        self.time_scale.pack(side="left", padx=10)
        
        # Control Buttons
        btn_frame = tk.Frame(control_frame, bg="#1c2230")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="⏸️ Pause", font=("Arial", 10, "bold"),
                  command=self.toggle_pause, bg="#ff6b6b", fg="white", width=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔁 Reset", font=("Arial", 10, "bold"),
                  command=self.reset_simulation, bg="#4ecdc4", fg="black", width=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="ℹ️ About", font=("Arial", 10, "bold"),
                  command=self.show_about, bg="#45b7d1", fg="white", width=8).pack(side="left", padx=5)

    def create_info_panel(self, parent):
        left_frame = tk.Frame(parent, bg="#1c2230", bd=2, relief="ridge")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header
        header_frame = tk.Frame(left_frame, bg="#1c2230")
        header_frame.pack(fill="x", pady=8)
        tk.Label(header_frame, text="🌠 Celestial Body Information", 
                font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack()
        
        # Information display
        info_frame = tk.Frame(left_frame, bg="#1c2230")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(info_frame, height=25, width=45,
                                                    wrap="word", font=("Consolas", 11),
                                                    bg="#0b0f1a", fg="white", 
                                                    insertbackground="white",
                                                    relief="flat", padx=10, pady=10)
        self.result_text.pack(fill="both", expand=True)

    def create_simulation_panel(self, parent):
        right_frame = tk.Frame(parent, bg="#0b0f1a", width=700, height=650)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)
        
        # Simulation header
        sim_header = tk.Frame(right_frame, bg="#1c2230")
        sim_header.pack(fill="x", pady=(0, 5))
        tk.Label(sim_header, text="🪐 Solar System Simulation", 
                font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=5)
        
        # Pygame frame
        self.pygame_frame = tk.Frame(right_frame, bg="black", relief="sunken", bd=2)
        self.pygame_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Instructions
        instruction_frame = tk.Frame(right_frame, bg="#0b0f1a")
        instruction_frame.pack(fill="x", pady=5)
        tk.Label(instruction_frame, text="💡 Click on any celestial body to select it", 
                font=("Arial", 10), fg="#ffffff", bg="#0b0f1a").pack()

    def create_status_bar(self):
        self.status = tk.Label(self.root, text="Ready - Select a celestial body to begin exploration", 
                              anchor="w", font=("Arial", 10), bg="#1c2230", fg="#00e6ff")
        self.status.pack(fill="x", side="bottom", ipady=3)

    def init_pygame(self):
        """Initialize Pygame in a thread-safe way"""
        try:
            # Embed Pygame in Tkinter frame
            os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())
            if sys.platform == "win32":
                os.environ['SDL_VIDEODRIVER'] = 'windib'
            
            pygame.init()
            self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(), 
                                                 self.pygame_frame.winfo_height()))
            pygame.display.set_caption("Solar System Simulation")
            self.pygame_initialized = True
            
            # Start the update loop
            self.update_pygame()
            
        except Exception as e:
            messagebox.showerror("Pygame Error", f"Could not initialize Pygame: {str(e)}")

    def on_search(self, event=None):
        query = self.search_var.get().strip().lower()
        if query:
            self.select_object(query)
            self.search_var.set("")

    def select_object(self, name):
        if name in SOLAR_SYSTEM:
            obj = SOLAR_SYSTEM[name]
            self.display_object_info(obj)
            self.highlight_object(obj)
            self.status.config(text=f"Selected: {obj.name} - {obj.get_info().split('Type: ')[1].split('\\n')[0]}")
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Object '{name}' not found.\n\nAvailable objects:\n" +
                                   "\n".join([f"• {body}" for body in SOLAR_SYSTEM.keys()]))
            self.status.config(text=f"Object '{name}' not found")

    def display_object_info(self, obj):
        self.result_text.delete("1.0", tk.END)
        info = obj.get_info()
        self.result_text.insert(tk.END, info)
        
        # Add some formatting
        self.result_text.tag_configure("title", foreground="#00e6ff", font=("Consolas", 11, "bold"))
        self.result_text.tag_configure("highlight", foreground="#ffcc00")
        
        # Apply formatting
        lines = info.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("Name:"):
                self.result_text.tag_add("title", f"1.0", f"1.{len(line)}")
            elif "Description:" in line:
                start_idx = f"{i+1}.0"
                self.result_text.tag_add("highlight", start_idx, f"{i+1}.end")

    def highlight_object(self, selected_obj):
        for body in PLANET_DATA:
            body.is_highlighted = (body == selected_obj)

    def set_time_factor(self, value):
        self.time_factor = float(value)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.time_scale.set(0)
        else:
            self.time_scale.set(0.5)

    def reset_simulation(self):
        for body in PLANET_DATA:
            body.angle = 0
        self.time_scale.set(0.5)
        self.time_factor = 0.5
        self.is_paused = False
        self.select_object("earth")

    def show_about(self):
        about_text = """
🌌 Celestial Explorer 🌌

An interactive solar system simulator that allows you to:
• Explore detailed information about celestial bodies
• Watch realistic orbital mechanics in action
• Click on planets and moons to select them
• Control simulation speed and pause/reset

Features:
• 8 celestial bodies including Sun, planets, and Moon
• Realistic orbital periods and distances (scaled)
• Detailed physical properties and descriptions
• Beautiful space-themed interface

Educational tool for astronomy enthusiasts and students!
        """
        messagebox.showinfo("About Celestial Explorer", about_text.strip())

    def handle_click(self, pos):
        """Handle mouse clicks in Pygame window"""
        for body in PLANET_DATA:
            if body.is_clicked(pos):
                self.select_object(body.name.lower())
                return True
        return False

    def update_pygame(self):
        if not self.pygame_initialized:
            return

        try:
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

            # Update and draw
            self.screen.fill(BLACK)
            
            # Draw background stars
            self.draw_stars()
            
            # Update positions and draw celestial bodies
            center_x, center_y = self.screen.get_width() / 2, self.screen.get_height() / 2
            
            for body in PLANET_DATA:
                if not self.is_paused:
                    body.update_position(self.time_factor, center_x, center_y)
                body.draw(self.screen, center_x, center_y)
            
            pygame.display.flip()
            
            # Continue the update loop
            self.root.after(30, self.update_pygame)
            
        except Exception as e:
            print(f"Pygame update error: {e}")
            # Try to reinitialize on error
            self.root.after(1000, self.update_pygame)

    def draw_stars(self):
        """Draw random stars in the background"""
        import random
        for _ in range(50):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)

    def on_resize(self, event):
        """Handle window resize"""
        if hasattr(self, 'screen') and self.pygame_initialized:
            try:
                self.screen = pygame.display.set_mode((event.width, event.height))
            except:
                pass

    def on_closing(self):
        """Clean up when closing the application"""
        if self.pygame_initialized:
            pygame.quit()
        self.root.destroy()


# ---------------------- #
# Main Execution
# ---------------------- #
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AstronomyApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"The application encountered an error:\n{str(e)}")