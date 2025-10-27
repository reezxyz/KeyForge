import keyboard
import time
import threading

def run_macro(profile):
    """Jalankan makro (Press/Release/Delay)"""
    actions = profile.get("actions", [])
    for action in actions:
        if action["type"] == "press":
            keyboard.press(action["key"])
        elif action["type"] == "release":
            keyboard.release(action["key"])
        elif action["type"] == "delay":
            time.sleep(action["duration"] / 1000)
