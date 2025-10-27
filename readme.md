# KeyForgePy

**KeyForgePy** is a modern **Keyboard Macro Manager** built with Python. It allows you to create, manage, and apply macros for **specific keyboards**, making it ideal for gaming, productivity, or custom automation scenarios.

---

## Features

- **Targeted Keyboard Support**: Only inputs from the selected keyboard trigger macros.
- **Macro Editor with Profiles**: Each profile can contain sequences of **press/release actions** with configurable delays.
- **Custom Input Simulation**: Control **initial delay** and **repeat interval** for simulated key presses.
- **Visual Keyboard Layout**: Shows a visual keyboard layout to easily assign macros.
- **Profile Management**: Save and load macro profiles in **JSON format**.
- **System Tray Support**: Minimize the application to the tray for quick access.
- **Modern GUI**: Built with **CustomTkinter** and **PySide6** for a sleek, contemporary interface.

---

## Requirements

- Python 3.11+  
- Python packages:  
  ```bash
  pip install customtkinter pynput keyboard PySide6 pyautogui

