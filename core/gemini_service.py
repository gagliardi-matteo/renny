import os
from dotenv import load_dotenv
from google import generativeai as genai

# Carica variabili da .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("⚠️ Nessuna API key trovata nel file .env (GOOGLE_API_KEY)")

# Configura Gemini (nuovo SDK)
genai.configure(api_key=API_KEY)

class GeminiService:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def text(self, prompt: str) -> str:
        try:
            print(f"[Gemini] ➜ Prompt inviato:\n{prompt}\n")
            response = self.model.generate_content(prompt)
            print(f"[Gemini] ⇦ Risposta ricevuta:\n{response.text}\n")
            return response.text.strip()
        except Exception as e:
            print(f"[Gemini] ❌ Errore: {e}")
            return "Bau... non riesco a connettermi a Gemini."
