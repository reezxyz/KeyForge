import customtkinter as ctk
from core.profiles import load_profiles
import json
import os
from tkinter import messagebox

ASSIGNMENTS_FILE = "data/assignments.json"

class KeyboardUI(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.assignments = self.load_assignments()
        self.selected_profile = None
        self.key_buttons = {}
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Keyboard Macro Mapper", font=("Arial", 18, "bold")).pack(pady=10)

        # Dropdown untuk pilih profil
        profiles = [p["name"] for p in load_profiles()]
        self.profile_dropdown = ctk.CTkOptionMenu(self, values=profiles, command=self.select_profile)
        self.profile_dropdown.pack(pady=5)

        # Frame keyboard
        self.keyboard_frame = ctk.CTkFrame(self)
        self.keyboard_frame.pack(pady=10)

        # Layout keyboard (QWERTY 100% sederhana)
        rows = [
            ["ESC","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","PRTSC","DEL"],
            ["`","1","2","3","4","5","6","7","8","9","0","-","=","BACK"],
            ["TAB","Q","W","E","R","T","Y","U","I","O","P","[","]","\\","INS"],
            ["CAPS","A","S","D","F","G","H","J","K","L",";","'","ENTER"],
            ["SHIFT","Z","X","C","V","B","N","M",",",".","/","SHIFT"],
            ["CTRL","WIN","ALT","SPACE","ALT","WIN","MENU","CTRL"]
        ]

        for r, row_keys in enumerate(rows):
            row_frame = ctk.CTkFrame(self.keyboard_frame)
            row_frame.pack(pady=2)
            for key in row_keys:
                width = 40
                if key in ["SPACE"]:
                    width = 400
                elif key in ["SHIFT","ENTER","BACK","TAB","CAPS"]:
                    width = 80
                btn = ctk.CTkButton(row_frame, text=key, width=width,
                                     command=lambda k=key: self.apply_macro(k))
                btn.pack(side="left", padx=2, pady=2)
                self.key_buttons[key] = btn

                # Highlight jika sudah ada assignment
                if key in self.assignments:
                    btn.configure(fg_color="#1e90ff")

        # Tombol simpan assignments
        ctk.CTkButton(self, text="Save Assignments", command=self.save_assignments).pack(pady=10)

    def select_profile(self, profile_name):
        self.selected_profile = profile_name

    def apply_macro(self, key):
        if not self.selected_profile:
            messagebox.showerror("Error", "Pilih profil makro dulu!")
            return
        self.assignments[key] = self.selected_profile
        self.key_buttons[key].configure(fg_color="#1e90ff")

    def load_assignments(self):
        if os.path.exists(ASSIGNMENTS_FILE):
            with open(ASSIGNMENTS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_assignments(self):
        os.makedirs(os.path.dirname(ASSIGNMENTS_FILE), exist_ok=True)
        with open(ASSIGNMENTS_FILE, "w") as f:
            json.dump(self.assignments, f, indent=4)
        messagebox.showinfo("Saved", "Assignments saved!")
