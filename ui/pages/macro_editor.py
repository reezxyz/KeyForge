import customtkinter as ctk
from tkinter import messagebox
from core.profiles import save_profile

class MacroEditor(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#1e1e2f")
        self.actions = []
        self.selected_index = None
        self._build_ui()

    def _build_ui(self):
        # Input Profil
        ctk.CTkLabel(self, text="Nama Profil", font=("Arial", 14, "bold"), text_color="#EEE").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, fg_color="#2c2c3e", text_color="#EEE", border_color="#444466")
        self.name_entry.pack(pady=5, fill="x", padx=10)

        # Input Action
        ctk.CTkLabel(self, text="Tambahkan Action", font=("Arial", 14, "bold"), text_color="#EEE").pack(pady=5)
        self.key_entry = ctk.CTkEntry(self, placeholder_text="Key", fg_color="#2c2c3e", text_color="#EEE", border_color="#444466")
        self.key_entry.pack(pady=2, fill="x", padx=10)

        self.type_var = ctk.CTkOptionMenu(self, values=["press", "release", "delay"], fg_color="#2c2c3e", button_color="#444466", button_hover_color="#555577")
        self.type_var.pack(pady=2, fill="x", padx=10)

        self.delay_entry = ctk.CTkEntry(self, placeholder_text="Delay ms (jika delay)", fg_color="#2c2c3e", text_color="#EEE", border_color="#444466")
        self.delay_entry.pack(pady=2, fill="x", padx=10)

        ctk.CTkButton(self, text="Tambah Action", command=self.add_action, fg_color="#444466", hover_color="#555577").pack(pady=5)

        # List Action
        self.action_frame = ctk.CTkFrame(self, fg_color="#2c2c3e")
        self.action_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.action_labels = []

        # Tombol kontrol urutan
        ctrl_frame = ctk.CTkFrame(self, fg_color="#1e1e2f")
        ctrl_frame.pack(pady=5)
        ctk.CTkButton(ctrl_frame, text="⬆ Move Up", width=100, fg_color="#444466", hover_color="#555577", command=self.move_up).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text="⬇ Move Down", width=100, fg_color="#444466", hover_color="#555577", command=self.move_down).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text="🗑 Hapus", width=100, fg_color="#884444", hover_color="#AA5555", command=self.delete_action).pack(side="left", padx=5)

        # Tombol simpan
        ctk.CTkButton(self, text="💾 Simpan Profil", command=self.save_profile, fg_color="#62825D", hover_color="#526E48").pack(pady=10)

    # ---------------- LOGIC ----------------
    def add_action(self):
        key = self.key_entry.get().strip()
        action_type = self.type_var.get()

        if action_type == "delay":
            try:
                duration = int(self.delay_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Delay harus berupa angka!")
                return
            action = {"type": "delay", "duration": duration}
        else:
            if not key:
                messagebox.showerror("Error", "Key harus diisi!")
                return
            action = {"type": action_type, "key": key}

        self.actions.append(action)
        self.key_entry.delete(0, "end")
        self.delay_entry.delete(0, "end")
        self.update_action_list()

    def update_action_list(self):
        for lbl in self.action_labels:
            lbl.destroy()
        self.action_labels.clear()

        for i, act in enumerate(self.actions):
            text = f"{i+1}. "
            if act["type"] == "delay":
                text += f"Delay {act['duration']} ms"
            else:
                text += f"{act['type']} {act['key']}"

            lbl = ctk.CTkLabel(self.action_frame, text=text, text_color="#EEE", fg_color="#2c2c3e", corner_radius=5)
            lbl.pack(fill="x", padx=5, pady=2)
            lbl.bind("<Button-1>", lambda e, idx=i: self.select_action(idx))
            self.action_labels.append(lbl)

            if self.selected_index == i:
                lbl.configure(fg_color="#444466")

    def select_action(self, idx):
        self.selected_index = idx
        self.update_action_list()

    def move_up(self):
        if self.selected_index is None or self.selected_index == 0:
            return
        self.actions[self.selected_index - 1], self.actions[self.selected_index] = (
            self.actions[self.selected_index],
            self.actions[self.selected_index - 1],
        )
        self.selected_index -= 1
        self.update_action_list()

    def move_down(self):
        if self.selected_index is None or self.selected_index >= len(self.actions) - 1:
            return
        self.actions[self.selected_index + 1], self.actions[self.selected_index] = (
            self.actions[self.selected_index],
            self.actions[self.selected_index + 1],
        )
        self.selected_index += 1
        self.update_action_list()

    def delete_action(self):
        if self.selected_index is not None and 0 <= self.selected_index < len(self.actions):
            del self.actions[self.selected_index]
            self.selected_index = None
            self.update_action_list()

    def save_profile(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Nama profil harus diisi!")
            return
        if not self.actions:
            messagebox.showerror("Error", "Tidak ada action untuk disimpan!")
            return

        profile = {"name": name, "actions": self.actions}
        save_profile(profile)
        messagebox.showinfo("Sukses", f"Profil '{name}' tersimpan!")
