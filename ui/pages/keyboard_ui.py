import customtkinter as ctk
import json
import os
from tkinter import messagebox
from core.profiles import load_profiles  # pastikan ada fungsi load_profiles
from core.listener import MacroListener

ASSIGNMENTS_FILE = "data/assignments.json"

class KeyboardUI(ctk.CTkFrame):
    """UI untuk assign makro ke tombol keyboard"""
    def __init__(self, master=None, listener=None):
        super().__init__(master, fg_color="#1e1e2f")  # background sesuai sidebar
        self.assignments = self.load_assignments()
        self.selected_profile = None
        self.key_buttons = {}
        self.listener = listener  # listener di-passing dari MainApp
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Keyboard Macro Mapper", font=("Arial", 18, "bold"),
                     text_color="#EEEEDD").pack(pady=10)

        # Dropdown untuk pilih profil
        profiles = [p["name"] for p in load_profiles()]
        self.profile_dropdown = ctk.CTkOptionMenu(
            self, values=profiles, command=self.select_profile,
            fg_color="#2c2c3e", button_color="#444466", button_hover_color="#555577"
        )
        self.profile_dropdown.pack(pady=5)

        # Frame keyboard
        self.keyboard_frame = ctk.CTkFrame(self, fg_color="#2c2c3e")
        self.keyboard_frame.pack(pady=10, fill="both", expand=True)

        # Layout keyboard sederhana
        rows = [
            ["ESC","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","PRTSC","DEL"],
            ["`","1","2","3","4","5","6","7","8","9","0","-","=","BACK"],
            ["TAB","Q","W","E","R","T","Y","U","I","O","P","[","]","\\"],
            ["CAPS","A","S","D","F","G","H","J","K","L",";","'","ENTER"],
            ["SHIFT","Z","X","C","V","B","N","M",",",".","/","SHIFT"],
            ["CTRL","WIN","ALT","SPACE","ALT","WIN","MENU","CTRL"]
        ]

        for row_keys in rows:
            row_frame = ctk.CTkFrame(self.keyboard_frame, fg_color="#2c2c3e")
            row_frame.pack(pady=2)
            for key in row_keys:
                width = 40
                if key in ["SPACE"]:
                    width = 400
                elif key in ["SHIFT","ENTER","BACK","TAB","CAPS"]:
                    width = 80
                btn = ctk.CTkButton(
                    row_frame, text=key, width=width,
                    fg_color="#444466", hover_color="#555577",
                    command=lambda k=key: self.apply_macro(k)
                )
                btn.pack(side="left", padx=2, pady=2)
                self.key_buttons[key] = btn

        # Tombol simpan assignments
        ctk.CTkButton(self, text="Save Assignments", command=self.save_assignments,
                      fg_color="#62825D", hover_color="#526E48").pack(pady=5)

        # Tombol Start / Stop Listener
        btn_frame = ctk.CTkFrame(self, fg_color="#1e1e2f")
        btn_frame.pack(pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start Listener", fg_color="#C2FFC7",
                                       hover_color="#9EDF9C", command=self.start_listener)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text="❌ Stop Listener", fg_color="#62825D",
                                      hover_color="#526E48", command=self.stop_listener)
        self.stop_btn.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(self, text="Listener belum aktif ❌", text_color="#EEEEDD")
        self.status_label.pack(pady=5)

    def select_profile(self, profile_name):
        self.selected_profile = profile_name
        for key, btn in self.key_buttons.items():
            if key in self.assignments and self.assignments[key] == profile_name:
                btn.configure(fg_color="#444466")
            else:
                btn.configure(fg_color="#2c2c3e")

    def apply_macro(self, key):
        if not self.selected_profile:
            messagebox.showerror("Error", "Pilih profil makro dulu!")
            return
        self.assignments[key] = self.selected_profile
        self.update_highlight()

    def update_highlight(self):
        for k, btn in self.key_buttons.items():
            if k in self.assignments and self.assignments[k] == self.selected_profile:
                btn.configure(fg_color="#444466")
            else:
                btn.configure(fg_color="#2c2c3e")

    def load_assignments(self):
        if os.path.exists(ASSIGNMENTS_FILE):
            with open(ASSIGNMENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_assignments(self):
        os.makedirs(os.path.dirname(ASSIGNMENTS_FILE), exist_ok=True)
        with open(ASSIGNMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.assignments, f, indent=4)
        messagebox.showinfo("Saved", "Assignments saved!")

    # ---------------- Listener control -----------------
    def start_listener(self):
        if self.listener:
            self.listener.assignments = self.assignments
            self.listener.start()
            self.status_label.configure(text="Listener aktif ✅")

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
            self.status_label.configure(text="Listener berhenti ❌")
