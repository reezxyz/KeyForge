# core/listener.py
import threading
import json
from pathlib import Path
import keyboard  # capture + suppress
from pynput.keyboard import Controller
from core.profiles import load_profile_by_name
import time

ASSIGNMENTS_FILE = Path("data/assignments.json")

kb_controller = Controller()

class MacroListener:
    def __init__(self, target_device_id=None):
        self.target_device_id = target_device_id  # string device ID HID
        self.assignments = {}
        self._running = False
        self._lock = threading.Lock()
        self._hook_threads = []

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
        """Eksekusi profile untuk key_name"""
        profile_name = self.assignments.get(key_name)
        if not profile_name:
            return
        profile = load_profile_by_name(profile_name)
        if not profile:
            return

        for action in profile.get("actions", []):
            if action.get("type") == "press":
                kb_controller.press(action["key"])
                kb_controller.release(action["key"])
            elif action.get("type") == "release":
                kb_controller.release(action["key"])
            elif action.get("type") == "delay":
                duration_ms = action.get("duration", 0)
                time.sleep(duration_ms / 1000.0)  # delay dalam detik


    def _hook_key(self, key_name):
        """Hook trigger key dengan suppress input asli"""
        def callback(event):
            if not self._running:
                return
            if event.event_type != "down":
                return
            # jalankan macro di thread terpisah
            threading.Thread(target=self._run_macro_for_key, args=(key_name,), daemon=True).start()

        # hook key dengan suppress=True
        keyboard.hook_key(key_name, callback, suppress=True)
        self._hook_threads.append(callback)

    def start(self):
        if not self.target_device_id:
            raise ValueError("Target device ID belum di-set!")

        with self._lock:
            if self._running:
                return
            self._running = True

        # hook semua keys yang memiliki assignments
        for key_name in self.assignments.keys():
            self._hook_key(key_name)

    def stop(self):
        with self._lock:
            self._running = False
        # unhook semua hook
        keyboard.unhook_all()
