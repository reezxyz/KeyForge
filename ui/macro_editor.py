import customtkinter as ctk
from tkinter import messagebox
from core.profiles import save_profile

class MacroEditor(ctk.CTkToplevel):
    """UI untuk buat / edit profil makro"""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Macro Editor")
        self.geometry("400x550")  # lebih tinggi supaya tombol terlihat
        self.actions = []

        self._build_ui()

    def _build_ui(self):
        # Nama profil
        ctk.CTkLabel(self, text="Nama Profil", font=("Arial", 14)).pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=5, fill="x", padx=10)

        # Tambah action
        ctk.CTkLabel(self, text="Tambahkan Action", font=("Arial", 14)).pack(pady=5)
        self.key_entry = ctk.CTkEntry(self, placeholder_text="Key")
        self.key_entry.pack(pady=2, fill="x", padx=10)

        self.type_var = ctk.CTkOptionMenu(self, values=["press","release","delay"])
        self.type_var.pack(pady=2, fill="x", padx=10)

        self.delay_entry = ctk.CTkEntry(self, placeholder_text="Delay ms (jika delay)")
        self.delay_entry.pack(pady=2, fill="x", padx=10)

        ctk.CTkButton(self, text="Tambah Action", command=self.add_action).pack(pady=5)

        # Frame scrollable untuk daftar actions
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=5, padx=10, fill="both", expand=True)
        action_frame.pack_propagate(False)

        self.actions_box = ctk.CTkTextbox(action_frame, height=200)
        self.actions_box.pack(fill="both", expand=True)

        # Tombol simpan selalu terlihat di bawah
        ctk.CTkButton(self, text="💾 Simpan Profil", command=self.save_profile).pack(pady=10)

    def add_action(self):
        key = self.key_entry.get()
        action_type = self.type_var.get()
        duration = self.delay_entry.get()

        if action_type == "delay":
            try:
                duration = int(duration)
            except:
                messagebox.showerror("Error", "Delay harus angka!")
                return
            action = {"type":"delay", "duration":duration}
        else:
            if not key:
                messagebox.showerror("Error", "Key harus diisi!")
                return
            action = {"type":action_type, "key":key.upper()}

        self.actions.append(action)
        self.update_actions_box()

    def update_actions_box(self):
        self.actions_box.delete("1.0", "end")
        for act in self.actions:
            if act["type"]=="delay":
                self.actions_box.insert("end", f"Delay {act['duration']} ms\n")
            else:
                self.actions_box.insert("end", f"{act['type'].capitalize()} {act['key']}\n")

    def save_profile(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Nama profil harus diisi!")
            return
        profile = {"name": name, "actions": self.actions}
        save_profile(profile)
        messagebox.showinfo("Sukses", f"Profil '{name}' tersimpan!")
        self.destroy()
