import customtkinter as ctk
from tkinter import messagebox
from core.profiles import save_profile

class MacroEditor(ctk.CTkFrame):
    def __init__(self, master=None):
        # fg_color sama dengan sidebar, ungu gelap
        super().__init__(master, fg_color="#1e1e2f")
        self.actions = []
        self._build_ui()

    def _build_ui(self):
        # Label dengan teks putih
        ctk.CTkLabel(self, text="Nama Profil", font=("Arial", 14), text_color="#EEE").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, fg_color="#2c2c3e", text_color="#EEE")
        self.name_entry.pack(pady=5, fill="x", padx=10)

        # Tambah action
        ctk.CTkLabel(self, text="Tambahkan Action", font=("Arial", 14), text_color="#EEE").pack(pady=5)
        self.key_entry = ctk.CTkEntry(self, placeholder_text="Key", fg_color="#2c2c3e", text_color="#EEE")
        self.key_entry.pack(pady=2, fill="x", padx=10)

        self.type_var = ctk.CTkOptionMenu(self, values=["press","release","delay"], fg_color="#2c2c3e")
        self.type_var.pack(pady=2, fill="x", padx=10)

        self.delay_entry = ctk.CTkEntry(self, placeholder_text="Delay ms (jika delay)", fg_color="#2c2c3e", text_color="#EEE")
        self.delay_entry.pack(pady=2, fill="x", padx=10)

        ctk.CTkButton(self, text="Tambah Action", command=self.add_action, fg_color="#444466").pack(pady=5)

        self.actions_box = ctk.CTkTextbox(self, height=200, fg_color="#2c2c3e", text_color="#EEE")
        self.actions_box.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkButton(self, text="💾 Simpan Profil", command=self.save_profile, fg_color="#444466").pack(pady=10)



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
