# asset.py
# Contains embedded image data for the login background wallpaper.
# The image will be stored as base64 so no external file paths are required.

import base64
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

def get_wallpaper_image():
    """Return a PhotoImage object of the embedded background."""
    img_data = b"""/9j/4AAQSkZJRgABAQEBLAEsAAD/4QBWRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAITAAMAAAABAAEAAAAAAAAAAAEsAAAAAQAAASwAAAAB/+0ALFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAAAPHAFaAAMbJUccAQAA"""
    image_bytes = base64.b64decode(img_data)
    image = Image.open(BytesIO(image_bytes))
    return ImageTk.PhotoImage(image)

if __name__ == "__main__":
    # Quick preview if you run this file directly
    root = tk.Tk()
    root.title("Wallpaper Preview")
    wallpaper = get_wallpaper_image()
    label = tk.Label(root, image=wallpaper)
    label.pack()
    root.mainloop()
