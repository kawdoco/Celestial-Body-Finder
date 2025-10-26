
# login_launcher.py
# Optional: pretty login screen that launches main.py after successful login.
# This mirrors your existing colorful login behavior and does not change app output.
import os, sys, hashlib, time, getpass, subprocess

TARGET_SCRIPT = "main.py"

_DEMO_USERS = {
    "admin": hashlib.sha256("1234".encode()).hexdigest(),
    "user": hashlib.sha256("pass".encode()).hexdigest(),
}

TK_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    TK_AVAILABLE = True
except Exception:
    tk = None; messagebox = None; ttk = None

def _sha256(txt: str) -> str:
    return hashlib.sha256(txt.encode()).hexdigest()

def _validate_credentials(username: str, password: str) -> bool:
    if not username or not password: return False
    return _DEMO_USERS.get(username) == _sha256(password)

def _abs_path(path: str) -> str:
    return path if os.path.isabs(path) else os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

def _run_target_script(path: str) -> None:
    path = _abs_path(path)
    if not os.path.exists(path):
        if TK_AVAILABLE and messagebox:
            messagebox.showerror("File not found", f"Could not locate:\n{path}")
        else:
            print(f"[ERROR] File not found: {path}", file=sys.stderr)
        return
    try:
        creationflags = 0
        if sys.platform.startswith("win"):
            creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen([sys.executable, path], creationflags=creationflags)
    except Exception as e:
        if TK_AVAILABLE and messagebox:
            messagebox.showerror("Launch error", f"Failed to start target script:\n{e}")
        else:
            print(f"[ERROR] Failed to start target script: {e}", file=sys.stderr)
    finally:
        os._exit(0)

def console_login():
    print("\n=== Secure Login (Console Mode) ===")
    print("Tip: demo credentials → admin/1234  •  user/pass")
    for attempt in range(3):
        user = input("Username: ").strip()
        passwd = getpass.getpass("Password: ")
        if _validate_credentials(user, passwd):
            print("\nLogin successful. Launching application...\n")
            time.sleep(0.4)
            _run_target_script(TARGET_SCRIPT)
            return
        else:
            print("Invalid credentials. Try again.\n")
    print("Too many failed attempts. Exiting.")

if TK_AVAILABLE:
    class ColorfulLogin(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("✨ Welcome | Secure Login ✨")
            self.geometry("900x600")
            self.minsize(820, 520)
            self.configure(bg="#0b0f1a")
            self._particles = []
            self._build_style()
            self._build_gradient()
            self._build_card()
            self._animate_background()
            self.bind("<Return>", lambda e: self._on_login())

        def _build_style(self):
            style = ttk.Style(self)
            try:
                style.theme_use("clam")
            except Exception:
                pass
            style.configure("TEntry", padding=8, fieldbackground="#E1E6F1")
            style.map("TEntry", fieldbackground=[("active", "#0f172a")])
            style.configure("Rounded.TButton", font=("Segoe UI", 12, "bold"), padding=12)
            style.configure("Glass.TFrame", background="#0b0f1a")
            style.configure("TCheckbutton", background="#0b0f1a", foreground="#dbeafe")
            style.configure("bar.Horizontal.TProgressbar", thickness=10)

        def _build_gradient(self):
            self.canvas = tk.Canvas(self, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.bind("<Configure>", lambda e: self._draw_gradient())

        def _draw_gradient(self):
            self.canvas.delete("grad")
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            stops = [
                (0.00, (11, 15, 26)),
                (0.35, (24, 24, 48)),
                (0.70, (33, 12, 74)),
                (1.00, (0, 78, 146)),
            ]
            def lerp(a, b, t): return int(a + (b - a) * t)
            for y in range(h):
                t = y / max(h - 1, 1)
                for i in range(len(stops) - 1):
                    if stops[i][0] <= t <= stops[i + 1][0]:
                        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
                        tt = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                        r = lerp(c0[0], c1[0], tt); g = lerp(c0[1], c1[1], tt); b = lerp(c0[2], c1[2], tt)
                        self.canvas.create_rectangle(0, y, w, y + 1,
                            fill=f"#{r:02x}{g:02x}{b:02x}", outline="", tags="grad")
                        break
            self._ensure_particles()

        def _ensure_particles(self):
            import random
            if getattr(self, "_particles", None):
                return
            w = max(self.canvas.winfo_width(), 900)
            h = max(self.canvas.winfo_height(), 600)
            self._particles = []
            for _ in range(80):
                x = random.randint(0, w); y = random.randint(0, h)
                size = random.choice([1, 1, 1, 2]); spd = random.uniform(0.1, 0.6)
                item = self.canvas.create_oval(x, y, x + size, y + size, fill="#ffffff", outline="", tags="star")
                self._particles.append((item, spd))

        def _animate_background(self):
            for item, spd in self._particles:
                self.canvas.move(item, spd, 0)
                x1, y1, x2, y2 = self.canvas.coords(item)
                w = self.canvas.winfo_width()
                if x1 > w:
                    self.canvas.move(item, -(w + 5), 0)
            self.after(30, self._animate_background)

        def _build_card(self):
            self.card = tk.Frame(self.canvas, bg="#0b0f1a")
            self.card_id = self.canvas.create_window(0, 0, window=self.card)
            self.canvas.bind("<Configure>", self._recenter)

            glass = tk.Frame(self.card, bg="#0d1224"); glass.pack(padx=28, pady=28)
            tk.Label(glass, text="🪐", font=("Segoe UI Emoji", 48), bg="#0d1224", fg="#e0e7ff").pack(pady=(12, 4))
            tk.Label(glass, text="Celestial Body Finder", font=("Poppins", 26, "bold"),
                     bg="#0d1224", fg="#a5b4fc").pack(pady=(0, 4))
            tk.Label(glass, text="Sign in to continue", font=("Segoe UI", 12),
                     bg="#0d1224", fg="#dbeafe").pack(pady=(0, 18))

            form = tk.Frame(glass, bg="#0d1224"); form.pack(padx=22, pady=10)

            tk.Label(form, text="Username", font=("Segoe UI", 10, "bold"),
                     bg="#0d1224", fg="#93c5fd").grid(row=0, column=0, sticky="w")
            self.username = ttk.Entry(form, width=32)
            self.username.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 12))

            tk.Label(form, text="Password", font=("Segoe UI", 10, "bold"),
                     bg="#0d1224", fg="#93c5fd").grid(row=2, column=0, sticky="w")
            self.password = ttk.Entry(form, width=28, show="●")
            self.password.grid(row=3, column=0, sticky="ew", pady=(2, 12))
            self._show = tk.BooleanVar(value=False)
            tk.Checkbutton(form, text="Show", variable=self._show, command=self._toggle_pw,
                           bg="#0d1224", fg="#e5e7eb", activebackground="#0d1224",
                           selectcolor="#0d1224").grid(row=3, column=1, sticky="w", padx=(10, 0))

            self.remember = tk.BooleanVar()
            tk.Checkbutton(glass, text="Remember me", variable=self.remember,
                           bg="#0d1224", fg="#d1d5db", activebackground="#0d1224",
                           selectcolor="#0d1224").pack(anchor="w", padx=22)

            tk.Button(glass, text="Login", font=("Segoe UI", 13, "bold"),
                      bg="#38bdf8", fg="#0b0f1a", activebackground="#67e8f9",
                      relief="flat", bd=0, padx=22, pady=10, cursor="hand2",
                      command=self._on_login).pack(fill="x", padx=22, pady=(12, 4))

            tk.Label(glass, text="Demo → admin / 1234  •  user / pass", font=("Segoe UI", 9),
                     bg="#0d1224", fg="#a1a1aa").pack(pady=(2, 6))

        def _recenter(self, _=None):
            w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
            self.canvas.coords(self.card_id, w // 2, h // 2)

        def _toggle_pw(self):
            self.password.configure(show="" if self._show.get() else "●")

        def _on_login(self):
            user = self.username.get().strip(); pwd = self.password.get()
            if not user or not pwd:
                self._toast("Please enter username and password."); return
            if not _validate_credentials(user, pwd):
                self._toast("Invalid credentials. Try again."); return
            self._show_success_and_launch()

        def _toast(self, msg: str):
            t = tk.Toplevel(self); t.overrideredirect(True); t.configure(bg="#ef4444")
            x = self.winfo_rootx() + self.winfo_width() // 2 - 130
            y = self.winfo_rooty() + self.winfo_height() // 2 + 140
            t.geometry(f"260x36+{x}+{y}")
            tk.Label(t, text=msg, bg="#ef4444", fg="white", font=("Segoe UI", 9, "bold")).pack(fill="both", expand=True)
            t.after(1600, t.destroy)

        def _show_success_and_launch(self):
            for w in (self.canvas, self.card): w.destroy()
            wrap = tk.Frame(self, bg="#0b0f1a"); wrap.pack(fill="both", expand=True)
            tk.Label(wrap, text="Welcome ✨", font=("Poppins", 24, "bold"),
                     bg="#0b0f1a", fg="#a7f3d0").pack(pady=(120, 10))
            tk.Label(wrap, text="Launching your application…", font=("Segoe UI", 12),
                     bg="#0b0f1a", fg="#c7d2fe").pack(pady=(0, 20))
            pb = ttk.Progressbar(wrap, mode="indeterminate", length=320, style="bar.Horizontal.TProgressbar")
            pb.pack(pady=10); pb.start(12)
            self.after(900, lambda: _run_target_script(TARGET_SCRIPT))

if __name__ == "__main__":
    if TK_AVAILABLE:
        app = ColorfulLogin()  # type: ignore
        app.mainloop()
    else:
        console_login()
