import cv2
import time
import google.generativeai as genai
from vilib import Vilib
from pidog import Pidog
from config.config import GEMINI_API_KEY

# ── Configurazione Gemini ────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# ── Setup PiDog e Camera ────────────────────────────────────────────────
dog = Pidog()
Vilib.camera_start(vflip=False, hflip=False)
time.sleep(2)

print("🤖 Vision system attivo. Premi Ctrl+C per uscire.")

def analyze_frame(frame):
    """Analizza un frame e restituisce l’interpretazione testuale."""
    _, img_bytes = cv2.imencode(".jpg", frame)
    img_bytes = img_bytes.tobytes()
    response = model.generate_content(
        [
            {"mime_type": "image/jpeg", "data": img_bytes},
            "Descrivi in italiano cosa sta succedendo nell'immagine in modo conciso."
        ]
    )
    return response.text.strip() if response.text else "Non riesco a capire cosa vedo."

def react_to_description(desc):
    """Reazione del cane in base alla descrizione visiva."""
    desc_low = desc.lower()
    print(f"👁️  {desc}")

    if any(word in desc_low for word in ["persona", "uomo", "donna", "bambino"]):
        dog.do_action("wag_tail", speed=80)
        dog.head_move([[0, 0, 20]], immediately=True)
        print("🐶: Ciao amico umano!")
    elif "palla" in desc_low:
        dog.do_action("walk", step_count=3)
        print("🐶: Una palla! Voglio giocarci!")
    elif "cibo" in desc_low or "ciotola" in desc_low:
        dog.do_action("sit")
        print("🐶: Ho fame!")
    else:
        dog.do_action("stand")
        print("🐶: Sto osservando l’ambiente...")

try:
    while True:
        frame = Vilib.get_frame()
        if frame is None:
            continue

        description = analyze_frame(frame)
        react_to_description(description)
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Terminato dall’utente.")
    Vilib.camera_close()
    dog.close()
