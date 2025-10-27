import customtkinter as ctk
from tkinter import messagebox
from core.profiles import save_profile, load_profiles

class MacroEditor(ctk.CTkFrame):
    """Page Macro Editor"""
    def __init__(self, master):
        super().__init__(master)
        self.actions = []
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Macro Editor", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Nama Profil").pack(pady=2)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=10)

        # Input Key Action
        self.key_entry = ctk.CTkEntry(self, placeholder_text="Key")
        self.key_entry.pack(fill="x", padx=10, pady=2)
        self.type_var = ctk.CTkOptionMenu(self, values=["press","release","delay"])
        self.type_var.pack(fill="x", padx=10, pady=2)
        self.delay_entry = ctk.CTkEntry(self, placeholder_text="Delay ms jika delay")
        self.delay_entry.pack(fill="x", padx=10, pady=2)

        ctk.CTkButton(self, text="Tambah Action", command=self.add_action).pack(pady=5)

        # Actions List
        self.actions_box = ctk.CTkTextbox(self, height=200)
        self.actions_box.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkButton(self, text="💾 Simpan Profil", command=self.save_profile).pack(pady=10)

    def add_action(self):
        key = self.key_entry.get()
        action_type = self.type_var.get()

        if action_type == "delay":
            try:
                duration = int(self.delay_entry.get())
            except:
                messagebox.showerror("Error", "Delay harus angka")
                return
            action = {"type":"delay", "duration":duration}
        else:
            if not key:
                messagebox.showerror("Error", "Key harus diisi")
                return
            action = {"type":action_type, "key":key}
        self.actions.append(action)
        self.update_actions_box()
        self.key_entry.delete(0,"end")

    def update_actions_box(self):
        self.actions_box.delete("1.0","end")
        for a in self.actions:
            if a["type"]=="delay":
                self.actions_box.insert("end", f"Delay {a['duration']} ms\n")
            else:
                self.actions_box.insert("end", f"{a['type']} {a['key']}\n")

    def save_profile(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Nama profil harus diisi")
            return
        profile = {"name": name, "actions": self.actions}
        save_profile(profile)
        messagebox.showinfo("Sukses", f"Profil '{name}' tersimpan")
