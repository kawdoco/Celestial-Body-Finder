import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D projection
import matplotlib.pyplot as plt
import numpy as np

# ----------------------
# Base Class
# ----------------------
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
                f"Mass: {self.mass} kg\n"
                f"Gravity: {self.gravity} m/s²\n"
                f"Radius: {self.radius} km\n")

# ----------------------
# Subclasses
# ----------------------
class Planet(CelestialObject):
    def __init__(self, name, mass, gravity, radius, has_life=False):
        super().__init__(name, "Planet", mass, gravity, radius)
        self.has_life = has_life

    def get_info(self):
        info = super().get_info()
        info += f"Supports Life: {'Yes' if self.has_life else 'No'}\n"
        return info


class Moon(CelestialObject):
    def __init__(self, name, mass, gravity, radius, planet):
        super().__init__(name, "Moon", mass, gravity, radius)
        self.planet = planet

    def get_info(self):
        info = super().get_info()
        info += f"Orbits: {self.planet}\n"
        return info


class Star(CelestialObject):
    def __init__(self, name, mass, gravity, radius, temperature):
        super().__init__(name, "Star", mass, gravity, radius)
        self.temperature = temperature

    def get_info(self):
        info = super().get_info()
        info += f"Surface Temperature: {self.temperature} K\n"
        return info


# ----------------------
# Dataset
# ----------------------
DATASET = {
    "earth": Planet("Earth", 5.97e24, 9.8, 6371, has_life=True),
    "mars": Planet("Mars", 6.39e23, 3.7, 3389, has_life=False),
    "moon": Moon("Moon", 7.35e22, 1.62, 1737, "Earth"),
    "jupiter": Planet("Jupiter", 1.898e27, 24.8, 69911),
    "sun": Star("Sun", 1.989e30, 274, 696340, 5778),
}

# ----------------------
# 3D Plot Helper
# ----------------------
def draw_3d_sphere(ax, radius):
    """Draw a sphere representing the celestial object"""
    ax.clear()
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, color="skyblue", edgecolor="black", linewidth=0.2, alpha=0.8)
    ax.set_box_aspect([1,1,1])
    ax.axis("off")
    ax.set_title("3D View", fontsize=14)

# ----------------------
# GUI Application
# ----------------------
class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astronomy Finder - 3D UI")
        self.root.geometry("900x500")

        # ---- Left Panel ----
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(left_frame, text="🔭 Astronomy OOP Project", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry = tk.Entry(left_frame, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.insert(0, "Earth")  # default

        self.button = tk.Button(left_frame, text="Search", command=self.search_object, font=("Arial", 12))
        self.button.pack(pady=5)

        self.result_text = tk.Text(left_frame, height=20, width=45, wrap="word", font=("Arial", 12))
        self.result_text.pack(pady=10)

        # ---- Right Panel (3D Canvas) ----
        self.fig = plt.Figure(figsize=(5,5))
        self.ax = self.fig.add_subplot(111, projection="3d")
        draw_3d_sphere(self.ax, 1)  # default sphere
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def search_object(self):
        name = self.entry.get().strip().lower()
        self.result_text.delete("1.0", tk.END)

        if name in DATASET:
            obj = DATASET[name]
            self.result_text.insert(tk.END, obj.get_info())

            # Scale 3D sphere radius (log scale for visibility)
            r = np.log10(obj.radius) / 3  # reduce size for display
            draw_3d_sphere(self.ax, r)
            self.canvas.draw()
        else:
            messagebox.showerror("Error", f"No data found for '{name}'")

# ----------------------
# Run
# ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
