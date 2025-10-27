import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    """Sidebar navigasi untuk switch page"""
    def __init__(self, master, menu_items, command):
        super().__init__(master, width=200, fg_color="#1e1e2f")
        self.pack(side="left", fill="y")
        self.command = command
        self.buttons = {}

        for item in menu_items:
            btn = ctk.CTkButton(
                self,
                text=item,
                width=200, height=40,
                fg_color="#2c2c3e",
                hover_color="#3b3b5c",
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
        for name, btn in self.buttons.items():
            btn.configure(fg_color="#2c2c3e" if name != item_name else "#444466")
        self.active_item = item_name
