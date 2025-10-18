import argparse
import subprocess
import sys
import os

# 🧩 forza il path principale del progetto (la cartella "renny")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run(script):
    script_path = os.path.join(PROJECT_ROOT, script)
    # imposta la directory di lavoro nel progetto principale
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT
    return subprocess.call([sys.executable, script_path], cwd=PROJECT_ROOT, env=env)

def main():
    parser = argparse.ArgumentParser(description="Renny Pidog - Modalità")
    parser.add_argument("--mode", choices=["voice-chat", "voice-move", "vision"], required=True)
    args = parser.parse_args()

    if args.mode == "voice-chat":
        run("scripts/voice_response.py")
    elif args.mode == "voice-move":
        run("scripts/voice_motion.py")
    elif args.mode == "vision":
        run("scripts/vision_interaction.py")

if __name__ == "__main__":
    main()
