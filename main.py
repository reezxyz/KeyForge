import customtkinter as ctk
from ui.keyboard_ui import KeyboardUI
from ui.macro_editor import MacroEditor
from ui.keyboard_selector import KeyboardSelector
from core.listener import MacroListener

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard Macro Manager")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Listener untuk makro
        self.listener = MacroListener()

        # --- Frame kiri: Keyboard Selector ---
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(self.left_frame, text="Keyboard Target", font=("Arial", 16, "bold")).pack(pady=5)

        self.keyboard_selector = KeyboardSelector(
            self.left_frame,
            on_select_callback=self.set_target_keyboard
        )
        self.keyboard_selector.pack(fill="y", expand=True)

        # --- Frame kanan: Keyboard UI + Macro Manager ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Tombol buka Macro Editor
        ctk.CTkButton(self.right_frame, text="📖 Macro Editor", command=self.open_macro_editor).pack(pady=10)

        # Keyboard UI
        self.keyboard_ui = KeyboardUI(self.right_frame)
        self.keyboard_ui.pack(fill="both", expand=True)

        # Tombol Start / Stop Listener
        btn_frame = ctk.CTkFrame(self.right_frame)
        btn_frame.pack(pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Start Listener", command=self.start_listener, state="disabled")
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text="❌ Stop Listener", command=self.stop_listener)
        self.stop_btn.pack(side="left", padx=5)

        # Label status
        self.status_label = ctk.CTkLabel(self.right_frame, text="Listener belum aktif ❌")
        self.status_label.pack(pady=5)

    # --- Callback dari KeyboardSelector ---
    def set_target_keyboard(self, hid_path):
        self.listener.target_device_id = hid_path
        print(f"DEBUG: Listener target_device_id = {hid_path}")
        # Enable tombol start
        self.start_btn.configure(state="normal")
        self.status_label.configure(text=f"Keyboard dipilih ✅\n{hid_path}")

    # --- Macro Editor ---
    def open_macro_editor(self):
        MacroEditor(self)

    # --- Start / Stop Listener ---
    def start_listener(self):
        self.keyboard_ui.save_assignments()  # Simpan assignments sebelum start
        self.listener.load_assignments()
        self.listener.start()
        self.status_label.configure(text="Listener aktif ✅")

    def stop_listener(self):
        self.listener.stop()
        self.status_label.configure(text="Listener berhenti ❌")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
