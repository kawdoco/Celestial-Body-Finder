
# app_ui.py
import os, sys, random
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pygame

from simulation import PLANET_DATA, SOLAR_SYSTEM, WHITE, BLACK

class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Celestial Body Finder - Interactive Solar System ✨")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0b0f1a")

        self.time_factor = 0.5
        self.is_paused = False
        self.pygame_initialized = False

        self.setup_ui()
        self.init_pygame()

        self.select_object("earth")

    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#0b0f1a")
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="🌌 Celestial Body Finder",
                 font=("Helvetica", 28, "bold"), fg="#00e6ff", bg="#0b0f1a").pack()
        tk.Label(title_frame, text="Interactive Solar System Simulator",
                 font=("Helvetica", 14), fg="#ffffff", bg="#0b0f1a").pack()

        self.create_search_frame()
        self.create_quick_access_buttons()
        self.create_control_panel()

        content_frame = tk.Frame(self.root, bg="#0b0f1a")
        content_frame.pack(fill="both", expand=True, pady=10, padx=15)

        self.create_info_panel(content_frame)
        self.create_simulation_panel(content_frame)
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

        header_frame = tk.Frame(left_frame, bg="#1c2230")
        header_frame.pack(fill="x", pady=8)
        tk.Label(header_frame, text="🌠 Celestial Body Information",
                 font=("Arial", 16, "bold"), fg="#00e6ff", bg="#1c2230").pack()

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

        sim_header = tk.Frame(right_frame, bg="#1c2230")
        sim_header.pack(fill="x", pady=(0, 5))
        tk.Label(sim_header, text="🪐 Solar System Simulation",
                 font=("Arial", 14, "bold"), fg="#00e6ff", bg="#1c2230").pack(pady=5)

        self.pygame_frame = tk.Frame(right_frame, bg="black", relief="sunken", bd=2)
        self.pygame_frame.pack(fill="both", expand=True, padx=5, pady=5)

        instruction_frame = tk.Frame(right_frame, bg="#0b0f1a")
        instruction_frame.pack(fill="x", pady=5)
        tk.Label(instruction_frame, text="💡 Click on any celestial body to select it",
                 font=("Arial", 10), fg="#ffffff", bg="#0b0f1a").pack()

    def create_status_bar(self):
        self.status = tk.Label(self.root, text="Ready - Select a celestial body to begin exploration",
                               anchor="w", font=("Arial", 10), bg="#1c2230", fg="#00e6ff")
        self.status.pack(fill="x", side="bottom", ipady=3)

    def init_pygame(self):
        try:
            os.environ['SDL_WINDOWID'] = str(self.pygame_frame.winfo_id())
            if sys.platform == "win32":
                os.environ['SDL_VIDEODRIVER'] = 'windib'

            pygame.init()
            self.screen = pygame.display.set_mode((self.pygame_frame.winfo_width(),
                                                   self.pygame_frame.winfo_height()))
            pygame.display.set_caption("Solar System Simulation")
            self.pygame_initialized = True
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
            self.status.config(text=f"Selected: {obj.name} - {obj.get_info().split('Type: ')[1].split('\n')[0]}")
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Object '{name}' not found.\n\nAvailable objects:\n" +
                                    "\n".join([f"• {body}" for body in SOLAR_SYSTEM.keys()]))
            self.status.config(text=f"Object '{name}' not found")

    def display_object_info(self, obj):
        self.result_text.delete("1.0", tk.END)
        info = obj.get_info()
        self.result_text.insert(tk.END, info)

        self.result_text.tag_configure("title", foreground="#00e6ff", font=("Consolas", 11, "bold"))
        self.result_text.tag_configure("highlight", foreground="#ffcc00")

        lines = info.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("Name:"):
                self.result_text.tag_add("title", f"1.0", f"1.{len(line)}")
            elif "Description:" in line:
                start_idx = f"{i+1}.0"
                self.result_text.tag_add("highlight", start_idx, f"{i+1}.end")

    def highlight_object(self, selected_obj):
        from simulation import PLANET_DATA
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
        from simulation import PLANET_DATA
        for body in PLANET_DATA:
            body.angle = 0
        self.time_scale.set(0.5)
        self.time_factor = 0.5
        self.is_paused = False
        self.select_object("earth")

    def show_about(self):
        about_text = """
🌌 Celestial Body Finder 🌌

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
        messagebox.showinfo("About Celestial Body Finder", about_text.strip())

    def handle_click(self, pos):
        from simulation import PLANET_DATA
        for body in PLANET_DATA:
            if body.is_clicked(pos):
                self.select_object(body.name.lower())
                return True
        return False

    def update_pygame(self):
        if not self.pygame_initialized:
            return

        try:
            import pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            self.screen.fill(BLACK)

            self.draw_stars()

            center_x, center_y = self.screen.get_width() / 2, self.screen.get_height() / 2

            from simulation import PLANET_DATA
            for body in PLANET_DATA:
                if not self.is_paused:
                    body.update_position(self.time_factor, center_x, center_y)
                body.draw(self.screen, center_x, center_y)

            pygame.display.flip()
            self.root.after(30, self.update_pygame)

        except Exception as e:
            print(f"Pygame update error: {e}")
            self.root.after(1000, self.update_pygame)

    def draw_stars(self):
        for _ in range(50):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            brightness = random.randint(100, 255)
            import pygame
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)

    def on_resize(self, event):
        if hasattr(self, 'screen') and self.pygame_initialized:
            try:
                import pygame
                self.screen = pygame.display.set_mode((event.width, event.height))
            except Exception:
                pass

    def on_closing(self):
        if self.pygame_initialized:
            pygame.quit()
        self.root.destroy()
