# core/listener.py
import threading
import json
from pathlib import Path
import keyboard  # pip install keyboard
from pynput.keyboard import Controller
from core.profiles import load_profile_by_name
import time

ASSIGNMENTS_FILE = Path("data/assignments.json")

kb_controller = Controller()

class MacroListener:
    def __init__(self, target_device_id=None):
        self.target_device_id = target_device_id
        self.assignments = {}  # key -> profile_name
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
        profile_name = self.assignments.get(key_name)
        if not profile_name:
            return
        profile = load_profile_by_name(profile_name)
        if not profile:
            return
        for action in profile.get("actions", []):
            typ = action.get("type")
            if typ == "press":
                kb_controller.press(action["key"])
            elif typ == "release":
                kb_controller.release(action["key"])
            elif typ == "delay":
                dur = action.get("duration", 0) / 1000
                time.sleep(dur)
            time.sleep(0.01)  # sedikit jeda antar action

    def _hook_key(self, key_name):
        """Hook key dengan suppress supaya tombol asli tidak muncul"""
        def callback(event):
            if not self._running:
                return
            if event.event_type != "down":
                return
            threading.Thread(target=self._run_macro_for_key, args=(key_name,), daemon=True).start()

        keyboard.hook_key(key_name, callback, suppress=True)
        self._hook_threads.append(callback)

    def start(self):
        if not self.target_device_id:
            print("Target keyboard belum di-set!")
            return

        with self._lock:
            if self._running:
                return
            self._running = True

        # hook semua tombol yang memiliki assignment
        for key_name in self.assignments.keys():
            self._hook_key(key_name)
        print("MacroListener aktif ✅")

    def stop(self):
        with self._lock:
            self._running = False
        keyboard.unhook_all()
        print("MacroListener berhenti ❌")
