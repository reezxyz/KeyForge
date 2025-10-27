import customtkinter as ctk
from tkinter import messagebox
from core.profiles import save_profile

class MacroEditor(ctk.CTkFrame):
    """Macro Editor UI, bisa embedded atau standalone"""

    def __init__(self, master=None, standalone=False):
        if standalone:
            # standalone window
            self.window = ctk.CTkToplevel(master)
            self.window.title("Macro Editor")
            self.window.geometry("400x550")
            container = self.window
        else:
            # embedded frame
            super().__init__(master)
            container = self

        self.container = container
        self.actions = []

        self._build_ui()

    def _build_ui(self):
        # --- Profil Name ---
        ctk.CTkLabel(self.container, text="Nama Profil", font=("Arial", 14)).pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.container)
        self.name_entry.pack(pady=5, fill="x", padx=10)

        # --- Key Action ---
        ctk.CTkLabel(self.container, text="Tambahkan Key Action", font=("Arial", 14)).pack(pady=5)
        self.key_entry = ctk.CTkEntry(self.container, placeholder_text="Key")
        self.key_entry.pack(pady=2, fill="x", padx=10)

        self.type_var = ctk.CTkOptionMenu(self.container, values=["press", "release"])
        self.type_var.pack(pady=2, fill="x", padx=10)

        ctk.CTkButton(self.container, text="Tambah Key Action", command=self.add_key_action).pack(pady=5)

        # --- Delay Action ---
        ctk.CTkLabel(self.container, text="Tambahkan Delay", font=("Arial", 14)).pack(pady=5)
        self.delay_entry = ctk.CTkEntry(self.container, placeholder_text="Delay ms")
        self.delay_entry.pack(pady=2, fill="x", padx=10)

        ctk.CTkButton(self.container, text="Tambah Delay", command=self.add_delay_action).pack(pady=5)

        # --- Scrollable Action Box ---
        action_frame = ctk.CTkFrame(self.container)
        action_frame.pack(pady=5, padx=10, fill="both", expand=True)
        action_frame.pack_propagate(False)

        self.actions_box = ctk.CTkTextbox(action_frame, height=200)
        self.actions_box.pack(fill="both", expand=True)

        # --- Save Button ---
        ctk.CTkButton(self.container, text="💾 Simpan Profil", command=self.save_profile).pack(pady=10)

    # --- Tambah Key Action ---
    def add_key_action(self):
        key = self.key_entry.get().strip()
        action_type = self.type_var.get()

        if not key:
            messagebox.showerror("Error", "Key harus diisi!")
            return

        action = {"type": action_type, "key": key}  # simpan sesuai input user
        self.actions.append(action)
        self.update_actions_box()
        self.key_entry.delete(0, "end")

    # --- Tambah Delay Action ---
    def add_delay_action(self):
        delay = self.delay_entry.get().strip()
        try:
            delay_ms = int(delay)
        except:
            messagebox.showerror("Error", "Delay harus angka!")
            return

        action = {"type": "delay", "duration": delay_ms}
        self.actions.append(action)
        self.update_actions_box()
        self.delay_entry.delete(0, "end")

    # --- Update Textbox ---
    def update_actions_box(self):
        self.actions_box.delete("1.0", "end")
        for act in self.actions:
            if act["type"] == "delay":
                self.actions_box.insert("end", f"Delay {act['duration']} ms\n")
            else:
                self.actions_box.insert("end", f"{act['type'].capitalize()} {act['key']}\n")

    # --- Save Profile ---
    def save_profile(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Nama profil harus diisi!")
            return

        profile = {"name": name, "actions": self.actions}
        save_profile(profile)
        messagebox.showinfo("Sukses", f"Profil '{name}' tersimpan!")

        if hasattr(self, "window"):  # tutup window jika standalone
            self.window.destroy()
