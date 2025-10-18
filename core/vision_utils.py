import sys
import speech_recognition as sr
from config.config import LANGUAGE

# ── ASR (Automatic Speech Recognition) ───────────────────────────────────────

_recognizer = sr.Recognizer()

def _default_mic():
    """Rileva il microfono di default (personalizzabile se serve)."""
    return sr.Microphone()

def listen_once(timeout: float = 6.0, phrase_time_limit: float = 8.0) -> str:
    """
    Ascolta una singola frase e restituisce il testo riconosciuto.
    """
    with _default_mic() as source:
        # Auto-calibrazione rumore ambiente
        _recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("🎤 Ascolto...")
        try:
            audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

    try:
        # 👇 lingua caricata da config/config.py (es. LANGUAGE="it-IT")
        txt = _recognizer.recognize_google(audio, language=LANGUAGE)
        print(f"👉 Hai detto: {txt}")
        return txt.strip().lower()
    except sr.UnknownValueError:
        print("❌ Non ho capito, riprova.")
        return ""
    except sr.RequestError as e:
        print(f"[ASR] Errore servizio STT: {e}", file=sys.stderr)
        return ""

def listen_loop(wake_word: str | None = None):
    """
    Generatore che produce frasi riconosciute.
    Se wake_word è impostata, attende prima il wake_word, poi restituisce le frasi successive.
    """
    while True:
        utterance = listen_once()
        if not utterance:
            continue

        if wake_word:
            if wake_word.lower() in utterance:
                from core.tts_utils import speak_async
                speak_async("Dimmi pure.")
                # Prossima frase utile dopo la wake word
                cmd = listen_once()
                if cmd:
                    yield cmd
            else:
                # ignora se non contiene la wake word
                continue
        else:
            yield utterance
