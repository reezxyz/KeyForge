# core/keyboards.py
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

RIM_TYPEKEYBOARD = 1
RIDI_DEVICENAME = 0x20000007

class RAWINPUTDEVICELIST(ctypes.Structure):
    _fields_ = [("hDevice", wintypes.HANDLE), ("dwType", wintypes.DWORD)]

def list_keyboards():
    num_devices = ctypes.c_uint(0)
    cbSize = ctypes.sizeof(RAWINPUTDEVICELIST)
    res = user32.GetRawInputDeviceList(None, ctypes.byref(num_devices), cbSize)
    if res != 0 or num_devices.value == 0:
        return []

    device_list = (RAWINPUTDEVICELIST * num_devices.value)()
    res = user32.GetRawInputDeviceList(device_list, ctypes.byref(num_devices), cbSize)
    if res == -1:
        return []

    keyboards = []
    for device in device_list:
        if device.dwType == RIM_TYPEKEYBOARD:
            name_size = ctypes.c_uint(256)
            name_buf = ctypes.create_unicode_buffer(256)
            user32.GetRawInputDeviceInfoW(device.hDevice, RIDI_DEVICENAME, name_buf, ctypes.byref(name_size))
            keyboards.append(name_buf.value)
    return keyboards

if __name__ == "__main__":
    for k in list_keyboards():
        print(k)
