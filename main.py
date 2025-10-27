import customtkinter as ctk
from ui.keyboard_ui import KeyboardUI
from ui.macro_editor import MacroEditor
from ui.keyboard_selector import KeyboardSelector
from core.listener import MacroListener

# ---------------- Sidebar -----------------
class Sidebar(ctk.CTkFrame):
    """Simple sidebar with menu items"""
    def __init__(self, master, menu_items, command):
        super().__init__(master, width=200, fg_color="#1f1f1f")
        self.pack(side="left", fill="y")
        self.command = command
        self.buttons = {}

        for item in menu_items:
            btn = ctk.CTkButton(
                self, text=item,
                width=200, height=40,
                fg_color="#2a2a2a",
                hover_color="#3a3a3a",
                corner_radius=0,
                command=lambda i=item: self.on_click(i)
            )
            btn.pack(pady=1)
            self.buttons[item] = btn

        self.active_item = None

    def on_click(self, item_name):
        self.set_active(item_name)
        self.command(item_name)

    def set_active(self, item_name):
        # update button colors
        for name, btn in self.buttons.items():
            if name == item_name:
                btn.configure(fg_color="#444444")  # active bg
            else:
                btn.configure(fg_color="#2a2a2a")
        self.active_item = item_name

# ---------------- Main App -----------------
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard Macro Manager")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Listener
        self.listener = MacroListener()

        # Sidebar
        menu_items = ["Keyboard Selector", "Macro Editor", "Keyboard UI"]
        self.sidebar = Sidebar(self, menu_items, self.show_frame)

        # Frame container kanan
        self.frame_container = ctk.CTkFrame(self)
        self.frame_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Buat semua frame tapi sembunyikan dulu
        self.frames = {}
        self.frames["Keyboard Selector"] = KeyboardSelector(self.frame_container, self.set_target_keyboard)
        self.frames["Macro Editor"] = MacroEditor(self.frame_container)
        self.frames["Keyboard UI"] = KeyboardUI(self.frame_container)

        for f in self.frames.values():
            f.pack(fill="both", expand=True)
            f.pack_forget()  # sembunyikan semua frame awalnya

        # Set default frame
        self.sidebar.set_active("Keyboard Selector")
        self.show_frame("Keyboard Selector")

        # Tombol Start / Stop Listener
        btn_frame = ctk.CTkFrame(self.frame_container)
        btn_frame.pack(side="bottom", pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start Listener", command=self.start_listener, state="disabled")
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text="❌ Stop Listener", command=self.stop_listener)
        self.stop_btn.pack(side="left", padx=5)

        # Label status
        self.status_label = ctk.CTkLabel(self.frame_container, text="Listener belum aktif ❌")
        self.status_label.pack(side="bottom", pady=5)

    # ---------------- Sidebar callback -----------------
    def show_frame(self, item_name):
        for f in self.frames.values():
            f.pack_forget()
        frame = self.frames.get(item_name)
        if frame:
            frame.pack(fill="both", expand=True)

    # ---------------- KeyboardSelector callback -----------------
    def set_target_keyboard(self, hid_path):
        self.listener.target_device_id = hid_path
        print(f"DEBUG: Listener target_device_id = {hid_path}")
        self.start_btn.configure(state="normal")
        self.status_label.configure(text=f"Keyboard dipilih ✅\n{hid_path}")

    # ---------------- Listener -----------------
    def start_listener(self):
        self.frames["Keyboard UI"].save_assignments()  # Simpan assignments sebelum start
        self.listener.load_assignments()
        self.listener.start()
        self.status_label.configure(text="Listener aktif ✅")

    def stop_listener(self):
        self.listener.stop()
        self.status_label.configure(text="Listener berhenti ❌")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
