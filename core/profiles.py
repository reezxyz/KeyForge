import os
import json

PROFILES_DIR = "data/profiles"

def save_profile(profile):
    """Simpan profil makro ke file JSON"""
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)
    path = os.path.join(PROFILES_DIR, f"{profile['name']}.json")
    with open(path, "w") as f:
        json.dump(profile, f, indent=4)

def load_profiles():
    """Load semua profil makro"""
    profiles = []
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)
    for file in os.listdir(PROFILES_DIR):
        if file.endswith(".json"):
            with open(os.path.join(PROFILES_DIR, file), "r") as f:
                profiles.append(json.load(f))
    return profiles

def load_profile_by_name(name):
    """Load profil berdasarkan nama"""
    path = os.path.join(PROFILES_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None
