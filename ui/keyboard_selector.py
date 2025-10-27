import customtkinter as ctk
import ctypes
from ctypes import wintypes

# --- Windows constants ---
RIM_TYPEKEYBOARD = 1
RIDI_DEVICENAME = 0x20000007

user32 = ctypes.windll.user32

class RAWINPUTDEVICELIST(ctypes.Structure):
    _fields_ = [
        ("hDevice", wintypes.HANDLE),
        ("dwType", wintypes.DWORD)
    ]

def list_keyboards():
    """List semua keyboard HID lengkap"""
    num_devices = ctypes.c_uint(0)
    cbSize = ctypes.sizeof(RAWINPUTDEVICELIST)
    user32.GetRawInputDeviceList(None, ctypes.byref(num_devices), cbSize)
    if num_devices.value == 0:
        return []

    device_list = (RAWINPUTDEVICELIST * num_devices.value)()
    user32.GetRawInputDeviceList(device_list, ctypes.byref(num_devices), cbSize)

    keyboards = []
    for device in device_list:
        if device.dwType == RIM_TYPEKEYBOARD:
            name_size = ctypes.c_uint(512)
            name_buf = ctypes.create_unicode_buffer(512)
            user32.GetRawInputDeviceInfoW(device.hDevice, RIDI_DEVICENAME, name_buf, ctypes.byref(name_size))
            keyboards.append((name_buf.value, device.hDevice))
    return keyboards

class KeyboardSelector(ctk.CTkFrame):
    """UI pilih keyboard target dengan radio button (otomatis set target)"""

    def __init__(self, master=None, on_select_callback=None):
        super().__init__(master)
        self.on_select_callback = on_select_callback
        self.keyboards = list_keyboards()
        self.selected_index = ctk.IntVar(value=-1)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Daftar Keyboard Terhubung", font=("Arial", 14, "bold")).pack(pady=5)

        scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=250)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Buat radio button untuk setiap keyboard
        for i, (hid, _) in enumerate(self.keyboards):
            rb = ctk.CTkRadioButton(
                scroll_frame,
                text=hid,
                variable=self.selected_index,
                value=i,
                command=self._on_select  # otomatis set saat klik
            )
            rb.pack(anchor="w", pady=2)

    def _on_select(self):
        idx = self.selected_index.get()
        hid_path, _ = self.keyboards[idx]
        if self.on_select_callback:
            self.on_select_callback(hid_path)  # langsung kirim ke listener
