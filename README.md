# 🌌 Celestial Body Finder – 3D & Video

An interactive **Tkinter-based astronomy explorer** that lets you search for planets, moons, and stars while displaying:

✨ **Detailed Information** (mass, gravity, radius, etc.)  
🪐 **3D Textured Models** rendered with **Matplotlib**  
🎥 **Short Video Clips** played inside the app using **VLC**

---

## 🚀 Features
- 🔭 **Search** for celestial objects like **Earth, Mars, Moon, Jupiter, Sun**.
- 🌠 **3D Visualization** with realistic planet textures.
- 🎬 **Video Playback** inside the Tkinter window.
- 🎨 **Creative UI**: dark space theme with neon highlights.

---

## 👥 Team Members
| Name                | username                         |
|----------------------|--------------------------------|
| **Hasarinda Wasalamudali** | Hasarinda98 |
| **Dananjana dewmini**  | dananjanadewmini801-alt               |
| **lasitha Nirmal**  |lasithanirmal11111-hub                 |
| **Thilanka Randil**  | thilankarandil        |
| **Shashan Fernando**  |shashanfernando200401512855-ctrl       |

## 📂 Project Structure

Celestial-Body-Finder/

│

├─ assets/ # Store textures & videos

│ ├─ earth_texture.jpg

│ ├─ earth.mp4

│ ├─ mars_texture.jpg

│ ├─ mars.mp4

│ └─ ... other textures/videos

│

├─ celestial_app_creative.py # Main application with modern UI

├─ celestial_app.py # Original simple UI (optional)

└─ README.md


---

## 🛠️ Requirements
Install the required Python packages:

```bash
pip install numpy pillow matplotlib python-vlc

⚠️ VLC Media Player must also be installed on your system
so that python-vlc can find the VLC backend.

▶️ Running the App

1.Clone this repository:
git clone https://github.com/<your-username>/Celestial-Body-Finder.git
cd Celestial-Body-Finder

2.Add texture images & MP4 videos to the assets folder
(e.g., earth_texture.jpg, earth.mp4).

3.Launch the app:
python celestial_app_creative.py

Type a name (e.g. earth, mars, sun) and click Search.
| Search Earth                             | 3D Model + Video                   |
| ---------------------------------------- | ---------------------------------- |
| ![Search Example](assets/example_ui.png) | ![3D Model](assets/example_3d.png) |

(Add your own screenshots to assets and update the links above.)

🌍 Supported Objects

| Object  | Type   | Extra Info            |
| ------- | ------ | --------------------- |
| Earth   | Planet | Supports life         |
| Mars    | Planet | Red planet            |
| Moon    | Moon   | Orbits Earth          |
| Jupiter | Planet | Gas giant             |
| Sun     | Star   | Surface Temp \~5778 K |

Add more objects by editing the DATASET dictionary in the code.

⚡ Platform Notes

Windows: uses player.set_hwnd() for VLC embedding.

Linux: replace with player.set_xwindow().

macOS: replace with player.set_nsobject().

💡 Future Enhancements

Integrate NASA API for live data.

Add more celestial objects and HD textures.

Include camera controls for 3D rotation/zoom.

📜 License

Released under the MIT License – free to use, modify, and share.

⭐ Acknowledgements

Tkinter
 for the GUI.

Matplotlib
 for 3D rendering.

Pillow
 for image processing.

python-vlc
 for video playback.

💫 Explore the universe in 3D right from your desktop!

---

✅ **Usage Tip:**  
If you paste this into a `README.md` on GitHub, Copilot can automatically suggest edits (e.g., adding shields.io badges, more screenshots, or installation steps) as you continue typing.


-------

 


