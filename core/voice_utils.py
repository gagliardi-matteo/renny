import time
import sys
import platform
import speech_recognition as sr
import pyttsx3
from config.config import LANGUAGE

# ── TTS ───────────────────────────────────────────────────────────────────────
_tts_engine = None
_selected_voice_id = None

def _init_tts():
    global _tts_engine, _selected_voice_id
    if _tts_engine:
        return
    _tts_engine = pyttsx3.init()
    # Prova a selezionare una voce IT se presente
    try:
        voices = _tts_engine.getProperty("voices")
        it_candidates = [v for v in voices if "it" in (v.languages or [b""]) or "ital" in v.name.lower()]
        if it_candidates:
            _selected_voice_id = it_candidates[0].id
            _tts_engine.setProperty("voice", _selected_voice_id)
        # leggero rallentamento per chiarezza
        rate = _tts_engine.getProperty("rate")
        _tts_engine.setProperty("rate", int(rate * 0.95))
    except Exception:
        pass

def speak(text: str):
    if not text:
        return
    _init_tts()
    try:
        _tts_engine.say(text)
        _tts_engine.runAndWait()
    except Exception as e:
        print(f"[TTS] Errore: {e}", file=sys.stderr)

# ── ASR ───────────────────────────────────────────────────────────────────────
_recognizer = sr.Recognizer()

def _default_mic():
    # Usa microfono di default; se vuoi fissarne uno, gestiscilo qui
    return sr.Microphone()

def listen_once(timeout: float = 6.0, phrase_time_limit: float = 8.0) -> str:
    with _default_mic() as source:
        # Auto calibrazione rumore ambiente (breve)
        _recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("🎤 Ascolto...")
        try:
            audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""
    try:
        txt = _recognizer.recognize_google(audio, language=LANGUAGE)
        print(f"👉 Hai detto: {txt}")
        return txt.strip().lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[ASR] Errore servizio STT: {e}", file=sys.stderr)
        return ""

def listen_loop(wake_word: str | None = None):
    """
    Generatore che produce frasi riconosciute.
    Se wake_word è impostata, attende prima il wake_word, poi ritorna le frasi successive.
    """
    while True:
        utterance = listen_once()
        if not utterance:
            continue
        if wake_word:
            if wake_word.lower() in utterance:
                speak("Dimmi pure.")
                # Prossima frase “utile”
                cmd = listen_once()
                if cmd:
                    yield cmd
            else:
                # ignora se non contiene la wake word
                continue
        else:
            yield utterance
