#!/usr/bin/env python3
import os
import sys
import subprocess

# ──────────────────────────────────────────────
# 🧩 Utility
# ──────────────────────────────────────────────

def print_section(title):
    print(f"\n\033[1;36m=== {title} ===\033[0m")

def run_command(command, desc=None):
    if desc:
        print(f"\033[1;33m→ {desc}\033[0m")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"\033[1;31m✗ Errore durante: {command}\033[0m")
        sys.exit(1)
    else:
        print(f"\033[1;32m✓ OK\033[0m")

# ──────────────────────────────────────────────
# 📦 Installazione librerie Python
# ──────────────────────────────────────────────

def install_python_packages():
    print_section("Installazione librerie Python")

    packages = [
        "google-generativeai",
        "speechrecognition",
        "pyttsx3",
        "pyaudio",
        "opencv-python",
        "pillow",
        "numpy==2.2.6",  # versione compatibile
        "git+https://github.com/sunfounder/robot-hat.git@v2.0",
        "git+https://github.com/sunfounder/vilib.git@picamera2",
        "git+https://github.com/sunfounder/pidog.git@master"
    ]

    python_exec = sys.executable
    for pkg in packages:
        run_command(f'"{python_exec}" -m pip install --upgrade {pkg}', f"Installo {pkg}")

# ──────────────────────────────────────────────
# 📁 Creazione struttura progetto
# ──────────────────────────────────────────────

def create_project_structure():
    print_section("Creazione struttura cartelle")
    dirs = ["config", "core", "scripts"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"📁 Cartella '{d}' pronta.")

    if not os.path.exists("config/config.py"):
        with open("config/config.py", "w") as f:
            f.write('GEMINI_API_KEY = "INSERISCI_LA_TUA_API_KEY"\n')
        print("🧠 File config/config.py creato (inserisci la tua API key)")

# ──────────────────────────────────────────────
# 🚀 Main
# ──────────────────────────────────────────────

def main():
    print("\033[1;35m🐾 Installazione Renny Pidog in corso...\033[0m")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 o superiore richiesto.")
        sys.exit(1)

    install_python_packages()
    create_project_structure()

    print_section("Installazione completata 🎉")
    print("Ora puoi modificare config/config.py con la tua API key Gemini e lanciare gli script in /scripts")

if __name__ == "__main__":
    main()
