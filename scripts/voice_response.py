from core.voice_utils import listen_loop
from core.gemini_service import GeminiService
from core.tts_utils import speak_async   # ✅ versione multipiattaforma
import re
import time

WAKE_WORD = "ciao"
MAX_CHARS = 300

def main():
    print("🐶 Renny è pronto! Dì 'Renni' per attirare la sua attenzione.")
    gemini = GeminiService()
    wake_active = False

    for text in listen_loop():
        if not text:
            continue

        text_lower = text.lower().strip()
        print(f"🗣️ Hai detto: {text_lower}")

        # 🔹 Attivazione
        if not wake_active:
            if WAKE_WORD in text_lower:
                print("🐾 Wake word rilevata → attivo.")
                speak_async("Bau! Eccomi, sono qui!")
                wake_active = True
            continue

        # 🔹 Disattivazione
        if any(word in text_lower for word in ["basta", "dormi", "riposa"]):
            speak_async("Va bene, mi metto tranquillo. Chiamami se hai bisogno, bau.")
            wake_active = False
            continue

        # 🔹 Uscita
        if "esci" in text_lower:
            speak_async("Ciao amico! A presto!")
            time.sleep(2)
            break

        # 🔹 Prompt con personalità canina
        prompt = f"""
        Sei Renni, un cane intelligente e affettuoso.
        Parla come un cane che capisce gli umani: allegro, curioso e dolce.
        Rispondi in modo breve e amichevole, come un cane che vuole fare compagnia.
        Domanda: {text}
        """

        reply = gemini.text(prompt)

        if reply:
            # Pulizia e taglio
            reply = re.sub(r'\*\*(.*?)\*\*', r'\1', reply)
            if len(reply) > MAX_CHARS:
                reply = reply[:MAX_CHARS] + "..."
            print(f"🤖 Renny: {reply}")
            speak_async(reply)
        else:
            speak_async("Non ho capito, puoi ripetere?")

if __name__ == "__main__":
    main()
