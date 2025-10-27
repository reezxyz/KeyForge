# core/listener.py
import threading
import json
from pathlib import Path
import keyboard
from pynput.keyboard import Controller
from core.profiles import load_profile_by_name
import time

ASSIGNMENTS_FILE = Path("data/assignments.json")
kb_controller = Controller()

class MacroListener:
    def __init__(self, target_device_id=None):
        self.target_device_id = target_device_id
        self.assignments = {}
        self._running = False
        self._lock = threading.Lock()
        self.load_assignments()

    def load_assignments(self):
        if ASSIGNMENTS_FILE.exists():
            with open(ASSIGNMENTS_FILE, "r", encoding="utf-8") as f:
                self.assignments = json.load(f)
        else:
            self.assignments = {}

    def save_assignments(self):
        ASSIGNMENTS_FILE.parent.mkdir(exist_ok=True)
        with open(ASSIGNMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.assignments, f, indent=4)

    def _run_macro_for_key(self, key_name):
        profile_name = self.assignments.get(key_name)
        if not profile_name:
            return
        profile = load_profile_by_name(profile_name)
        if not profile:
            return
        for action in profile.get("actions", []):
            if action["type"] == "press":
                kb_controller.press(action["key"])
            elif action["type"] == "release":
                kb_controller.release(action["key"])
            elif action["type"] == "delay":
                time.sleep(action["duration"]/1000)

    def _hook_key(self, key_name):
        def callback(event):
            if not self._running or event.event_type != "down":
                return
            threading.Thread(target=self._run_macro_for_key, args=(key_name,), daemon=True).start()
        keyboard.hook_key(key_name, callback, suppress=True)

    def start(self):
        if not self.target_device_id:
            raise ValueError("Target device ID belum di-set!")
        with self._lock:
            self._running = True
        for key_name in self.assignments.keys():
            self._hook_key(key_name)

    def stop(self):
        with self._lock:
            self._running = False
        keyboard.unhook_all()
