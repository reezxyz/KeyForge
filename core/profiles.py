# core/profiles.py
import json
from pathlib import Path

PROFILES_FILE = Path("data/profiles.json")

def load_profiles():
    if PROFILES_FILE.exists():
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_profile(profile):
    profiles = load_profiles()
    # replace if name exists
    profiles = [p for p in profiles if p["name"] != profile["name"]]
    profiles.append(profile)
    PROFILES_FILE.parent.mkdir(exist_ok=True)
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4)

def load_profile_by_name(name):
    profiles = load_profiles()
    for p in profiles:
        if p["name"] == name:
            return p
    return None
