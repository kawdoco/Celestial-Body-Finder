import os
import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import vlc

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

ASSET_DIR = "assets"


# ---------------------- #
# Main App
# ---------------------- #
class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Celestial Explorer ✨")
        self.root.geometry("1200x780")
        self.root.configure(bg="#0b0f1a")
        self.player = None
        self.icons = {}  # store image references to avoid garbage collection

        # Title
        tk.Label(
            root, text="🌌 Celestial Body Finder",
            font=("Orbitron", 26, "bold"), fg="#00e6ff", bg="#0b0f1a"
        ).pack(pady=15)

        # --- Image Buttons ---
        btn_frame = tk.Frame(root, bg="#0b0f1a")
        btn_frame.pack(pady=10)
        self.create_icon_buttons(btn_frame)

        # Search Bar
        search_frame = tk.Frame(root, bg="#1c2230", bd=2, relief="ridge")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="🔭 Search Object:",
                 font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack(side="left", padx=10)

        self.entry = tk.Entry(search_frame, font=("Arial", 16), width=20,
                              bg="#111522", fg="white")
        self.entry.pack(side="left", padx=10)
        self.entry.insert(0, "earth")

        tk.Button(search_frame, text="Search",
                  font=("Arial", 14, "bold"),
                  bg="#00e6ff", fg="black",
                  activebackground="#008fb3",
                  command=self.search_object).pack(side="left", padx=10)

        # Content Frames
        content_frame = tk.Frame(root, bg="#0b0f1a")
        content_frame.pack(fill="both", expand=True, pady=10)

        # Left Panel - Info + Video
        left_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="🌠 Object Information",
                 font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=10)

        self.result_text = tk.Text(left_frame, height=10, width=50,
                                   wrap="word", font=("Consolas", 13),
                                   bg="#0b0f1a", fg="white", insertbackground="white")
        self.result_text.pack(pady=10)

        tk.Label(left_frame, text="🎥 Video Preview",
                 font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=10)

        self.video_frame = tk.Frame(left_frame, width=480, height=270, bg="black")
        self.video_frame.pack(pady=10)

        # Right Panel - 3D Visualization
        right_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="🪐 3D Visualization",
                 font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=10)

        self.plot_frame = tk.Frame(right_frame, bg="#0b0f1a")
        self.plot_frame.pack(pady=10)

    def create_icon_buttons(self, parent):
        """Create image buttons for Earth, Mars, Moon, Jupiter, Sun"""
        for name in ["earth", "mars", "moon", "jupiter", "sun"]:
            icon_path = os.path.join(ASSET_DIR, f"{name}_icon.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path).resize((80, 80))
                icon = ImageTk.PhotoImage(img)
                self.icons[name] = icon  # keep a reference
                tk.Button(parent, image=icon, bg="#0b0f1a",
                          activebackground="#1c2230",
                          command=lambda n=name: self.quick_search(n)).pack(side="left", padx=10)

    def quick_search(self, name):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, name)
        self.search_object()

    def search_object(self):
        name = self.entry.get().strip().lower()
        self.result_text.delete("1.0", tk.END)

        if name not in DATASET:
            messagebox.showerror("Error", f"No data found for '{name}'")
            return

        obj = DATASET[name]
        self.result_text.insert(tk.END, obj.get_info())

        self.show_3d_planet(name)
        self.play_video(name)

    def show_3d_planet(self, name):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        texture_path = os.path.join(ASSET_DIR, f"{name}_texture.jpg")
        if not os.path.exists(texture_path):
            tk.Label(self.plot_frame, text="No texture image found.",
                     font=("Arial", 12), fg="white", bg="#0b0f1a").pack()
            return

        img = np.array(Image.open(texture_path).resize((360,180))) / 255.0
        fig = plt.Figure(figsize=(5,5), dpi=100, facecolor="#0b0f1a")
        ax = fig.add_subplot(111, projection='3d')

        u = np.linspace(0, 2*np.pi, img.shape[1])
        v = np.linspace(0, np.pi, img.shape[0])
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))

        ax.plot_surface(x, y, z, rstride=5, cstride=5,
                        facecolors=img[::-1,:,:], linewidth=0, antialiased=False)
        ax.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def play_video(self, name):
        if self.player:
            self.player.stop()

        video_path = os.path.join(ASSET_DIR, f"{name}.mp4")
        for widget in self.video_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(video_path):
            tk.Label(self.video_frame, text="No video file found.",
                     font=("Arial", 12), bg="black", fg="white").pack()
            return

        instance = vlc.Instance()
        self.player = instance.media_player_new()
        self.player.set_hwnd(self.video_frame.winfo_id())  # Windows only
        media = instance.media_new(video_path)
        self.player.set_media(media)
        self.player.play()


# ---------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
