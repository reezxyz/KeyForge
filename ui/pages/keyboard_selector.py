import customtkinter as ctk
from core.keyboards import list_keyboards

class KeyboardSelector(ctk.CTkFrame):
    """Page untuk pilih keyboard target"""
    def __init__(self, master, on_select_callback):
        super().__init__(master)
        self.on_select_callback = on_select_callback
        self.selected = None
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Keyboard Selector", font=("Arial", 18, "bold")).pack(pady=10)
        self.keyboard_list_frame = ctk.CTkFrame(self)
        self.keyboard_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_btn = ctk.CTkButton(self, text="Refresh List", command=self.populate_list)
        self.refresh_btn.pack(pady=5)

        self.populate_list()

    def populate_list(self):
        # Clear frame
        for widget in self.keyboard_list_frame.winfo_children():
            widget.destroy()

        keyboards = list_keyboards()
        if not keyboards:
            ctk.CTkLabel(self.keyboard_list_frame, text="Tidak ada keyboard terdeteksi").pack(pady=5)
            return

        for k in keyboards:
            btn = ctk.CTkButton(
                self.keyboard_list_frame,
                text=k,
                command=lambda k=k: self.select_keyboard(k)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def select_keyboard(self, keyboard_name):
        self.selected = keyboard_name
        if self.on_select_callback:
            self.on_select_callback(keyboard_name)
