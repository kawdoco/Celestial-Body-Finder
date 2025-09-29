# celestial_body_explorer_3d.py
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# Optional VLC for videos
try:
    import vlc
    VLC_AVAILABLE = True
except Exception:
    VLC_AVAILABLE = False

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
# Built-in dataset
# ---------------------- #
DATASET = {
    "earth": Planet("Earth", 5.97e24, 9.8, 6371, has_life=True),
    "mars": Planet("Mars", 6.39e23, 3.7, 3389),
    "moon": Moon("Moon", 7.35e22, 1.62, 1737, "Earth"),
    "jupiter": Planet("Jupiter", 1.898e27, 24.8, 69911),
    "sun": Star("Sun", 1.989e30, 274, 696340, 5778),
}

# Assets folder
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
ASSET_DIR = os.path.join(BASE_DIR, "assets")

# ---------------------- #
# Main App
# ---------------------- #
class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Celestial Explorer 3D ✨")
        self.root.geometry("1200x780")
        self.root.configure(bg="#0b0f1a")
        self.player = None
        self.vlc_instance = None

        # Title
        tk.Label(root, text="🌌 Celestial Body Finder",
                 font=("Helvetica", 26, "bold"), fg="#00e6ff", bg="#0b0f1a").pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(root, bg="#1c2230", bd=2, relief="ridge")
        search_frame.pack(pady=8, fill="x", padx=12)
        tk.Label(search_frame, text="🔭 Search Object:",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(side="left", padx=8)
        self.entry = tk.Entry(search_frame, font=("Arial", 14), width=20,
                              bg="#111522", fg="white", insertbackground="white")
        self.entry.pack(side="left", padx=8)
        self.entry.insert(0, "earth")
        tk.Button(search_frame, text="Search",
                  font=("Arial", 12, "bold"), bg="#00e6ff", fg="black",
                  activebackground="#008fb3", command=self.search_object).pack(side="left", padx=8)

        # Content Frames
        content_frame = tk.Frame(root, bg="#0b0f1a")
        content_frame.pack(fill="both", expand=True, pady=6, padx=12)

        # Left - Info + Video
        left_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        left_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        tk.Label(left_frame, text="🌠 Object Information",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=8)
        self.result_text = tk.Text(left_frame, height=12, width=48,
                                   wrap="word", font=("Consolas", 12),
                                   bg="#0b0f1a", fg="white", insertbackground="white")
        self.result_text.pack(pady=6, padx=8)
        tk.Label(left_frame, text="🎥 Video Preview",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=8)
        self.video_frame = tk.Frame(left_frame, width=480, height=270, bg="black")
        self.video_frame.pack(pady=6)
        self.video_frame.pack_propagate(False)

        # Right - 3D plot
        right_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        right_frame.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        tk.Label(right_frame, text="🪐 3D Visualization",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=8)
        self.plot_frame = tk.Frame(right_frame, bg="#0b0f1a")
        self.plot_frame.pack(padx=8, pady=6, fill="both", expand=True)

        # Status bar
        self.status = tk.Label(root, text="Ready", anchor="w", bg="#0b0f1a", fg="white")
        self.status.pack(fill="x", side="bottom")

    def search_object(self):
        self.result_text.delete("1.0", tk.END)
        name = self.entry.get().strip().lower()
        if not name:
            messagebox.showinfo("Info", "Please enter an object name.")
            return
        if name not in DATASET:
            messagebox.showerror("Error", f"No data found for '{name}'")
            return

        obj = DATASET[name]
        self.result_text.insert(tk.END, obj.get_info())
        self.status.config(text=f"Showing: {obj.name}")
        self.show_3d_object(obj)

    def show_3d_object(self, obj):
        for w in self.plot_frame.winfo_children():
            w.destroy()

        fig = plt.Figure(figsize=(5, 5), dpi=100, facecolor="#0b0f1a")
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#0b0f1a")

        # Sphere mesh
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = obj.radius * np.outer(np.cos(u), np.sin(v))
        y = obj.radius * np.outer(np.sin(u), np.sin(v))
        z = obj.radius * np.outer(np.ones_like(u), np.cos(v))

        ax.plot_surface(x, y, z, color="blue" if obj.object_type=="Planet" else "yellow",
                        edgecolor="k", linewidth=0.3, alpha=0.8)

        ax.set_box_aspect([1, 1, 1])
        ax.axis("off")
        ax.view_init(elev=30, azim=30)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
