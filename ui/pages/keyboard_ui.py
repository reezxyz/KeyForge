import customtkinter as ctk
import json
import os
from tkinter import messagebox

ASSIGNMENTS_FILE = "data/assignments.json"

class KeyboardUI(ctk.CTkFrame):
    """Page Keyboard UI untuk assign profile"""
    def __init__(self, master):
        super().__init__(master)
        self.assignments = self.load_assignments()
        self.selected_profile = None
        self.key_buttons = {}
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Keyboard UI", font=("Arial", 18, "bold")).pack(pady=10)

        from core.profiles import load_profiles
        profiles = [p["name"] for p in load_profiles()]
        self.profile_dropdown = ctk.CTkOptionMenu(self, values=profiles, command=self.select_profile)
        self.profile_dropdown.pack(pady=5)

        # Simple keyboard layout
        keys = ["A","B","C","D","E","F","G","H","I","J","K","L"]
        row_frame = ctk.CTkFrame(self)
        row_frame.pack(pady=5)
        for k in keys:
            btn = ctk.CTkButton(row_frame, text=k, width=40, command=lambda k=k: self.apply_macro(k))
            btn.pack(side="left", padx=2)
            self.key_buttons[k] = btn
            if k in self.assignments:
                btn.configure(fg_color="#1e90ff")

        ctk.CTkButton(self, text="Save Assignments", command=self.save_assignments).pack(pady=10)

    def select_profile(self, profile_name):
        self.selected_profile = profile_name

    def apply_macro(self, key):
        if not self.selected_profile:
            messagebox.showerror("Error", "Pilih profil dulu")
            return
        self.assignments[key] = self.selected_profile
        self.key_buttons[key].configure(fg_color="#1e90ff")

    def load_assignments(self):
        if os.path.exists(ASSIGNMENTS_FILE):
            with open(ASSIGNMENTS_FILE,"r") as f:
                return json.load(f)
        return {}

    def save_assignments(self):
        os.makedirs(os.path.dirname(ASSIGNMENTS_FILE), exist_ok=True)
        with open(ASSIGNMENTS_FILE,"w") as f:
            json.dump(self.assignments,f,indent=4)
        messagebox.showinfo("Saved","Assignments saved")
