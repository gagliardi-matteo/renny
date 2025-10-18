import os
import platform
import threading
import pyttsx3

def speak(text):
    """Parla in modo compatibile con Windows e Raspberry."""
    system = platform.system().lower()

    if "windows" in system:
        _speak_windows(text)
    else:
        _speak_linux(text)

def _speak_windows(text):
    """TTS con pyttsx3 (offline)."""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        voices = engine.getProperty('voices')
        for v in voices:
            if "it" in v.id.lower() or "lucia" in v.id.lower():
                engine.setProperty('voice', v.id)
                break
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS][Windows] Errore: {e}")

def _speak_linux(text):
    """TTS con pico2wave (offline, fluido su Raspberry)."""
    try:
        safe_text = text.replace('"', "'")
        os.system(f'pico2wave -l=it-IT -w=/tmp/tts.wav "{safe_text}" && aplay -q /tmp/tts.wav')
    except Exception as e:
        print(f"[TTS][Linux] Errore: {e}")

def speak_async(text):
    """Esegue il parlato in thread separato per non bloccare l’ascolto."""
    threading.Thread(target=speak, args=(text,), daemon=True).start()
