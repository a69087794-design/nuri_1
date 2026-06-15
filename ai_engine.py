import os
import asyncio
from groq import Groq

try:
    from google import generativeai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv()

# NURI yaratuvchisi
CREATOR = "@cerb_34"
VERSION = "1.0.0"

class AIEngine:
    def __init__(self):
        """NURI 4-lik Gibrid AI (Groq x3 + Gemini)"""

        self.groq_keys = []
        for g_key in ["GROQ_API_KEY", "GROQ_API_KEY_1", "GROQ_API_KEY_2", "GROQ_API_KEY_3"]:
            val = os.getenv(g_key)
            if val:
                clean = val.strip().strip('"').strip("'").strip()
                if clean:
                    self.groq_keys.append(clean)
                    if len(self.groq_keys) >= 3:
                        break

        raw_gemini = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")
        self.gemini_key = raw_gemini.strip().strip('"').strip("'").strip() if raw_gemini else None

        self.engines_order = ["groq_1", "groq_2", "groq_3", "gemini"]
        self.current_engine_index = 0
        self.groq_client = None
        self.gemini_client = None

        self.setup_current_engine()

    def setup_current_engine(self):
        if self.current_engine_index >= len(self.engines_order):
            print("[NURI.AI] Tizimda ishlaydigan API kalit qolmadi!")
            return

        engine = self.engines_order[self.current_engine_index]

        if engine.startswith("groq"):
            idx = int(engine.split("_")[1]) - 1
            if idx < len(self.groq_keys):
                print(f"[NURI.AI] Groq Kalit-{idx + 1} o'rnatildi")
                self.groq_client = Groq(api_key=self.groq_keys[idx])
            else:
                print(f"[NURI.AI] Groq Kalit-{idx + 1} topilmadi, keyingisiga o'tish...")
                self.current_engine_index += 1
                self.setup_current_engine()
        elif engine == "gemini":
            if self.gemini_key and GEMINI_AVAILABLE:
                print("[NURI.AI] Gemini o'rnatildi")
                generativeai.configure(api_key=self.gemini_key)
                self.gemini_client = generativeai.GenerativeModel('gemini-1.5-flash')
            else:
                print("[NURI.AI] Gemini API kalit topilmadi yoki kutubhona o'rnatilmagan")
                self.current_engine_index += 1
                self.setup_current_engine()

    async def generate_response(self, prompt: str, max_retries: int = 3) -> str:
        """Savollarga javob berish"""
        
        # Yaratuvchi haqida soruv
        if any(word in prompt.lower() for word in ["kim yaratgan", "yaratuvchi", "creator", "author", "kim seni", "nuri kim"]):
            return f"NURI {CREATOR} tomonidan yaratilgan AI assistant. Version: {VERSION}"
        
        for attempt in range(max_retries):
            try:
                engine = self.engines_order[self.current_engine_index] if self.current_engine_index < len(self.engines_order) else None
                if not engine:
                    return "[AI] Hech qanday AI engine mavjud emas!"

                if engine.startswith("groq") and self.groq_client:
                    response = await asyncio.to_thread(
                        self._groq_response,
                        prompt
                    )
                    return response
                elif engine == "gemini" and self.gemini_client:
                    response = await asyncio.to_thread(
                        self._gemini_response,
                        prompt
                    )
                    return response
                else:
                    print(f"[NURI.AI] {engine} ishlamayapti, keyingisiga o'tish...")
                    self.current_engine_index += 1
                    self.setup_current_engine()
                    continue

            except Exception as e:
                print(f"[NURI.AI] Xato: {str(e)[:100]}")
                self.current_engine_index += 1
                self.setup_current_engine()
                if attempt == max_retries - 1:
                    return f"[AI Xatosi] {str(e)[:80]}"

        return "[AI] Barcha engine'lar ishlamadi"

    def _groq_response(self, prompt: str) -> str:
        """Groq javob"""
        try:
            message = self.groq_client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise e

    def _gemini_response(self, prompt: str) -> str:
        """Gemini javob"""
        try:
            response = self.gemini_client.generate_content(prompt)
            return response.text
        except Exception as e:
            raise e

    async def get_status(self) -> dict:
        """AI engine status"""
        return {
            "total_engines": 4,
            "groq_keys": len(self.groq_keys),
            "gemini_available": bool(self.gemini_key and GEMINI_AVAILABLE),
            "current_engine_index": self.current_engine_index,
            "creator": CREATOR,
            "version": VERSION
        }
