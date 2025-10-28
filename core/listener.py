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

    # ---------------- MACRO EXECUTION ----------------
    def _run_macro_for_key(self, key_name):
        profile_name = self.assignments.get(key_name)
        if not profile_name:
            return

        profile = load_profile_by_name(profile_name)
        if not profile:
            return

        actions = profile.get("actions", [])
        i = 0
        while i < len(actions):
            act = actions[i]
            typ = act.get("type")

            # --------- CASE 1: press + delay + release (hold simulation) ----------
            if (
                typ == "press"
                and i + 2 < len(actions)
                and actions[i + 1]["type"] == "delay"
                and actions[i + 2]["type"] == "release"
                and actions[i + 2]["key"] == act["key"]
            ):
                key = act["key"]
                dur = actions[i + 1].get("duration", 0) / 1000
                self._simulate_hold_with_repeat(key, dur)
                i += 3
                continue

            # --------- CASE 2: normal single actions ----------
            if typ == "press":
                kb_controller.press(act["key"])
            elif typ == "release":
                kb_controller.release(act["key"])
            elif typ == "delay":
                time.sleep(act.get("duration", 0) / 1000)

            time.sleep(0.01)
            i += 1

    def _simulate_hold_with_repeat(self, key, duration, initial_delay=0.4, repeat_interval=0.06):
        """
        Meniru perilaku tombol yang ditekan lama (auto-repeat).
        """
        # satu input awal
        kb_controller.press(key)
        kb_controller.release(key)

        # jeda sebelum repeat
        if initial_delay > 0:
            time.sleep(initial_delay)

        # waktu akhir hold
        end_time = time.time() + max(0, duration - initial_delay)
        while time.time() < end_time and self._running:
            kb_controller.press(key)
            kb_controller.release(key)
            time.sleep(repeat_interval)

    # ---------------- HOOK SYSTEM ----------------
    def _hook_key(self, key_name):
        def callback(event):
            if not self._running or event.event_type != "down":
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

        for key_name in self.assignments.keys():
            self._hook_key(key_name)
        print("MacroListener aktif ✅")

    def stop(self):
        with self._lock:
            self._running = False
        keyboard.unhook_all()
        print("MacroListener berhenti ❌")
