import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from core.voice_utils import listen_loop, speak
from core.motion_utils import wag_tail, sit, lie_down, come_here, turn_left, turn_right, stop
from config.config import WAKE_WORD

def dispatch(cmd: str) -> bool:
    """
    Esegue il comando; ritorna True se riconosciuto.
    """
    if "siedi" in cmd or "siediti" in cmd:
        sit(); speak("Mi siedo!")
    elif "terra" in cmd or "sdraiati" in cmd or "a terra" in cmd:
        lie_down(); speak("Mi sdraio!")
    elif "vieni" in cmd or "qui" in cmd:
        come_here(); speak("Vengo da te!")
    elif "sinistra" in cmd:
        turn_left(); speak("Giro a sinistra!")
    elif "destra" in cmd:
        turn_right(); speak("Giro a destra!")
    elif "scodinzola" in cmd or "felice" in cmd:
        wag_tail(); speak("Scodinzolo felice!")
    elif "stop" in cmd or "fermo" in cmd:
        stop(); speak("Mi fermo!")
    else:
        return False
    return True

def main():
    speak("Pronto ai comandi!")
    for text in listen_loop(wake_word=WAKE_WORD):
        if any(x in text for x in ["esci", "chiudi", "termina"]):
            speak("Chiudo i comandi. A presto!")
            break
        ok = dispatch(text)
        if not ok:
            speak("Non ho capito. Puoi ripetere?")

if __name__ == "__main__":
    main()
