# celestial_body_finder_fix.py
import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib
# make sure TkAgg backend is used (FigureCanvasTkAgg requires Tk)
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Ensure 3D is available
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# Try importing vlc (video support). If it's missing we disable video.
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

# locate assets folder relative to the script (works if run from different cwd)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        BASE_DIR = os.getcwd()

ASSET_DIR = os.path.join(BASE_DIR, "assets")

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
        self.icons = {}          # keep PhotoImage refs
        self.canvas_refs = {}    # keep FigureCanvas refs (avoid GC)
        self.vlc_instance = None

        # Title
        tk.Label(
            root, text="🌌 Celestial Body Finder",
            font=("Helvetica", 26, "bold"), fg="#00e6ff", bg="#0b0f1a"
        ).pack(pady=10)

        # Top icon buttons
        btn_frame = tk.Frame(root, bg="#0b0f1a")
        btn_frame.pack(pady=8)
        self.create_icon_buttons(btn_frame)

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
                  font=("Arial", 12, "bold"),
                  bg="#00e6ff", fg="black",
                  activebackground="#008fb3",
                  command=self.search_object).pack(side="left", padx=8)

        tk.Button(search_frame, text="Check assets",
                  font=("Arial", 10),
                  command=self.check_assets).pack(side="right", padx=8)

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

        # video canvas
        self.video_frame = tk.Frame(left_frame, width=480, height=270, bg="black")
        self.video_frame.pack(pady=6)
        # ensure the video frame has a fixed size
        self.video_frame.pack_propagate(False)

        # Right - 3D plot
        right_frame = tk.Frame(content_frame, bg="#1c2230", bd=2, relief="ridge")
        right_frame.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        tk.Label(right_frame, text="🪐 3D Visualization",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=8)

        self.plot_frame = tk.Frame(right_frame, bg="#0b0f1a")
        self.plot_frame.pack(padx=8, pady=6, fill="both", expand=True)

        # status bar
        self.status = tk.Label(root, text="Ready", anchor="w", bg="#0b0f1a", fg="white")
        self.status.pack(fill="x", side="bottom")

    def log(self, text):
        """Log to result_text and console (keeps last entries visible)."""
        print(text)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)

    def create_icon_buttons(self, parent):
        """Create image buttons for Earth, Mars, Moon, Jupiter, Sun.
           If icon missing, create a text button instead."""
        for name in ["earth", "mars", "moon", "jupiter", "sun"]:
            icon_path = os.path.join(ASSET_DIR, f"{name}_icon.png")
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).convert("RGBA").resize((80, 80))
                    icon = ImageTk.PhotoImage(img)
                    self.icons[name] = icon  # keep ref
                    btn = tk.Button(parent, image=icon, bg="#0b0f1a",
                                    activebackground="#1c2230",
                                    bd=0, command=lambda n=name: self.quick_search(n))
                except Exception as e:
                    print(f"Error loading icon {icon_path}: {e}")
                    btn = tk.Button(parent, text=name.title(), bg="#0b0f1a",
                                    fg="white", command=lambda n=name: self.quick_search(n))
            else:
                # fallback: text button
                btn = tk.Button(parent, text=name.title(), bg="#0b0f1a",
                                fg="white", command=lambda n=name: self.quick_search(n))
            btn.pack(side="left", padx=10)

    def quick_search(self, name):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, name)
        self.search_object()

    def search_object(self):
        # Clear previous output
        self.result_text.delete("1.0", tk.END)
        name = self.entry.get().strip().lower()
        if not name:
            messagebox.showinfo("Info", "Please enter an object name.")
            return

        if name not in DATASET:
            messagebox.showerror("Error", f"No data found for '{name}'")
            return

        obj = DATASET[name]
        try:
            self.result_text.insert(tk.END, obj.get_info())
            self.status.config(text=f"Showing: {obj.name}")
            # show 3D (catch exceptions)
            try:
                self.show_3d_planet(name)
            except Exception as e:
                self.log("3D render error:")
                self.log(traceback.format_exc())

            # play video (if available)
            try:
                self.play_video(name)
            except Exception as e:
                self.log("Video playback error:")
                self.log(traceback.format_exc())

        except Exception as e:
            self.log("Unexpected error in search_object:")
            self.log(traceback.format_exc())
            messagebox.showerror("Error", "An unexpected error occurred. See details in the info box.")

    def show_3d_planet(self, name):
        # Remove old plot
        for w in self.plot_frame.winfo_children():
            w.destroy()
        if name is None:
            return

        texture_path = os.path.join(ASSET_DIR, f"{name}_texture.jpg")
        if not os.path.exists(texture_path):
            self.log(f"No texture found for '{name}' at {texture_path}.")
            tk.Label(self.plot_frame, text="No texture image found.", font=("Arial", 12),
                     fg="white", bg="#0b0f1a").pack(padx=10, pady=10)
            return

        # Load and map texture to sphere
        try:
            img_raw = Image.open(texture_path).convert("RGB")
            # keep aspect ratio -> make (width,height) consistent
            img = np.array(img_raw.resize((360, 180))) / 255.0

            fig = plt.Figure(figsize=(5, 5), dpi=100, facecolor="#0b0f1a")
            ax = fig.add_subplot(111, projection="3d")
            u = np.linspace(0, 2*np.pi, img.shape[1])
            v = np.linspace(0, np.pi, img.shape[0])
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones_like(u), np.cos(v))

            # map texture (flip vertically so it appears correctly)
            facecolors = img[::-1, :, :]

            ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=facecolors,
                            linewidth=0, antialiased=False)
            ax.set_axis_off()
            ax.view_init(elev=20, azim=30)

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(fill="both", expand=True)
            # keep reference to avoid GC
            self.canvas_refs[name] = canvas
        except Exception:
            self.log("Failed rendering 3D texture:")
            self.log(traceback.format_exc())
            tk.Label(self.plot_frame, text="Failed to render 3D (see info box).",
                     font=("Arial", 12), fg="white", bg="#0b0f1a").pack(padx=10, pady=10)

    def play_video(self, name):
        # stop previous player
        if self.player:
            try:
                self.player.stop()
            except Exception:
                pass
            self.player = None

        video_path = os.path.join(ASSET_DIR, f"{name}.mp4")
        for w in self.video_frame.winfo_children():
            w.destroy()

        if not VLC_AVAILABLE:
            self.log("python-vlc not installed; video playback disabled.")
            tk.Label(self.video_frame, text="Video playback not available (python-vlc missing).",
                     font=("Arial", 11), bg="black", fg="white").pack(padx=8, pady=8)
            return

        if not os.path.exists(video_path):
            self.log(f"No video file for '{name}': {video_path}")
            tk.Label(self.video_frame, text="No video file found.", font=("Arial", 12),
                     bg="black", fg="white").pack(padx=8, pady=8)
            return

        try:
            # ensure instance
            if not self.vlc_instance:
                self.vlc_instance = vlc.Instance()

            self.player = self.vlc_instance.media_player_new()
            media = self.vlc_instance.media_new(video_path)
            self.player.set_media(media)

            # platform-specific set-window
            handle = self.video_frame.winfo_id()
            try:
                if sys.platform.startswith("win"):
                    self.player.set_hwnd(handle)
                elif sys.platform.startswith("linux"):
                    self.player.set_xwindow(handle)
                elif sys.platform == "darwin":
                    # macOS: may not work in all environments. Wrap in try.
                    try:
                        self.player.set_nsobject(handle)
                    except Exception:
                        # fallback: no video embedding
                        self.log("macOS embedding failed; video will be played externally.")
                        self.player = None
                        os.startfile(video_path) if hasattr(os, "startfile") else os.system(f'open "{video_path}"')
                        return
            except Exception:
                # If embedding fails, attempt to open external player as fallback
                self.log("Embedding video into Tk failed; trying external player.")
                self.log(traceback.format_exc())
                try:
                    if hasattr(os, "startfile"):
                        os.startfile(video_path)
                    else:
                        # linux / mac
                        opener = "xdg-open" if sys.platform.startswith("linux") else "open"
                        os.system(f'{opener} "{video_path}" &')
                except Exception:
                    self.log("External video open also failed.")
                return

            # play
            self.player.play()
            self.status.config(text=f"Playing video for {name.title()}")
        except Exception:
            self.log("Error starting video playback:")
            self.log(traceback.format_exc())
            tk.Label(self.video_frame, text="Video playback failed (see info box).",
                     font=("Arial", 11), bg="black", fg="white").pack(padx=8, pady=8)

    def check_assets(self):
        """Quick check: lists which textures/icons/videos exist"""
        self.result_text.delete("1.0", tk.END)
        self.log(f"Assets directory: {ASSET_DIR}")
        for name in ["earth", "mars", "moon", "jupiter", "sun"]:
            icon = os.path.exists(os.path.join(ASSET_DIR, f"{name}_icon.png"))
            tex  = os.path.exists(os.path.join(ASSET_DIR, f"{name}_texture.jpg"))
            vid  = os.path.exists(os.path.join(ASSET_DIR, f"{name}.mp4"))
            self.log(f"{name:7s} | icon: {'Y' if icon else 'N'} | texture: {'Y' if tex else 'N'} | video: {'Y' if vid else 'N'}")
        if not VLC_AVAILABLE:
            self.log("python-vlc is NOT installed. Videos will not play until you install python-vlc and VLC player.")
        else:
            self.log("python-vlc available.")

# ---------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
