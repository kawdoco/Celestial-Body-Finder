import tkinter as tk
from tkinter import messagebox

# ----------------------
# Base Class
# ----------------------
class CelestialObject:
    def _init_(self, name, object_type, mass, gravity, radius):
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
    def _init_(self, name, mass, gravity, radius, has_life=False):
        super()._init_(name, "Planet", mass, gravity, radius)
        self.has_life = has_life

    def get_info(self):
        info = super().get_info()
        info += f"Supports Life: {'Yes' if self.has_life else 'No'}\n"
        return info


class Moon(CelestialObject):
    def _init_(self, name, mass, gravity, radius, planet):
        super()._init_(name, "Moon", mass, gravity, radius)
        self.planet = planet

    def get_info(self):
        info = super().get_info()
        info += f"Orbits: {self.planet}\n"
        return info


class Star(CelestialObject):
    def _init_(self, name, mass, gravity, radius, temperature):
        super()._init_(name, "Star", mass, gravity, radius)
        self.temperature = temperature

    def get_info(self):
        info = super().get_info()
        info += f"Surface Temperature: {self.temperature} K\n"
        return info


# ----------------------
# Built-in Dataset
# ----------------------
DATASET = {
    "earth": Planet("Earth", 5.97e24, 9.8, 6371, has_life=True),
    "mars": Planet("Mars", 6.39e23, 3.7, 3389, has_life=False),
    "moon": Moon("Moon", 7.35e22, 1.62, 1737, "Earth"),
    "jupiter": Planet("Jupiter", 1.898e27, 24.8, 69911),
    "sun": Star("Sun", 1.989e30, 274, 696340, 5778),
}


# ----------------------
# GUI Application
# ----------------------
class AstronomyApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Astronomy Finder (OOP, No API)")
        self.root.geometry("500x400")

        tk.Label(root, text="🔭 Astronomy OOP Project", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.insert(0, "Earth")  # default value

        self.button = tk.Button(root, text="Search", command=self.search_object, font=("Arial", 12))
        self.button.pack(pady=5)

        self.result_text = tk.Text(root, height=15, width=55, wrap="word", font=("Arial", 12))
        self.result_text.pack(pady=10)

    def search_object(self):
        name = self.entry.get().strip().lower()
        self.result_text.delete("1.0", tk.END)

        if name in DATASET:
            obj = DATASET[name]
            self.result_text.insert(tk.END, obj.get_info())
        else:
            messagebox.showerror("Error", f"No data found for '{name}'")


# ----------------------
# Run
# ----------------------
if _name_ == "_main_":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()