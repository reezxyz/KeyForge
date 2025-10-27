import customtkinter as ctk
from core.listener import MacroListener
from ui.pages.keyboard_selector import KeyboardSelector
from ui.pages.macro_editor import MacroEditor
from ui.pages.keyboard_ui import KeyboardUI
from ui.components.sidebar import Sidebar

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard Macro Manager")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.listener = MacroListener()

        menu = ["Keyboard Selector","Macro Editor","Keyboard UI"]
        self.sidebar = Sidebar(self, menu, self.show_frame)

        self.frame_container = ctk.CTkFrame(self)
        self.frame_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Buat semua frame
        self.frames = {}
        self.frames["Keyboard Selector"] = KeyboardSelector(self.frame_container, self.set_target_keyboard)
        self.frames["Macro Editor"] = MacroEditor(self.frame_container)
        self.frames["Keyboard UI"] = KeyboardUI(self.frame_container)

        for f in self.frames.values():
            f.pack(fill="both", expand=True)
            f.pack_forget()

        # Default page
        self.sidebar.set_active("Keyboard Selector")
        self.show_frame("Keyboard Selector")

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        frame = self.frames.get(name)
        if frame:
            frame.pack(fill="both", expand=True)

    def set_target_keyboard(self, device_name):
        self.listener.target_device_id = device_name
        print(f"Target keyboard: {device_name}")

if __name__=="__main__":
    app = MainApp()
    app.mainloop()
