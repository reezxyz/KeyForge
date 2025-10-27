import time
from pynput.keyboard import Controller

kb = Controller()

def run_macro(actions):
    for act in actions:
        if act["type"] == "press":
            kb.press(act["key"])
            kb.release(act["key"])
        elif act["type"] == "release":
            kb.release(act["key"])
        elif act["type"] == "delay":
            time.sleep(act["duration"] / 1000)  # durasi dalam ms
