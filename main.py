
# main.py
# Entry point that launches the Celestial Explorer UI (no login).
# Keeps the same runtime output as your original app.
import tkinter as tk
from app.ui import AstronomyApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()
