import os
import asyncio
from groq import Groq

# Ovoz yozish drayverlarini WSL uchun xavfsiz import qilish
try:
    import sounddevice as sd
    import scipy.io.wavfile as wav
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

class VoiceEngine:
    def __init__(self):
        """NURI Ovozli kirish va chiqish moduli (WSL-xavfsiz versiyasi)"""
        raw_key = os.getenv("GROQ_API_KEY_1")
        self.api_key = raw_key.strip('"').strip("'") if raw_key else None
        self.temp_audio_file = "temp_voice.wav"
        self.groq_client = None

        if self.api_key and AUDIO_AVAILABLE:
            try:
                self.groq_client = Groq(api_key=self.api_key)
                print("[NURI.VOICE] Groq Whisper va Audio drayverlar faol.")
            except Exception as e:
                print(f"[NURI.VOICE] Groq audio mijozida xato: {e}")
        else:
            print("[NURI.VOICE] Ovozli rejim (STT) vaqtincha nofaol. CLI/Matn rejimida davom etamiz.")

    async def speak(self, text: str):
        """
        Matnni ovozga aylantirish (TTS)
        WSL muhitida audio pleyerlar osilib qolishini oldini olish uchun
        hozircha matn interfeysiga xavfsiz yo'naltirildi.
        """
        if not text or not text.strip():
            return
        
        # WSL ichida alsa/pulse drayverlari bloklanib qolmasligi uchun 
        # asinxron zanjirni buzmaydigan mikro-kutish beramiz
        await asyncio.sleep(0.05)
        return

    async def listen_groq_whisper(self, duration: int = 4) -> str:
        """Mikrofondan ovozni asinxron yozib olib, Groq Whisper orqali matnga o'girish"""
        # Agar kalit bo'lmasa yoki drayver yuklanmagan bo'lsa, siklni qizdirib yubormaslik uchun kutib qaytamiz
        if not self.groq_client or not AUDIO_AVAILABLE:
            await asyncio.sleep(1.5)
            return ""

        fs = 16000  # Whisper modeli tushunadigan standart chastota
        try:
            loop = asyncio.get_event_loop()
            
            # Ovoz yozish jarayoni asosiy asinxron siklni bloklab qo'ymasligi kerak
            def record_audio():
                try:
                    # Windows mikrofoni ulanmagan bo'lsa, bu yerda xato berishi mumkin
                    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
                    sd.wait()
                    return recording
                except Exception:
                    return None

            recording = await loop.run_in_executor(None, record_audio)
            
            if recording is None:
                await asyncio.sleep(1.0)
                return ""

            # Vaqtincha WAV faylga yozamiz
            wav.write(self.temp_audio_file, fs, recording)

            # Groq API ga asinxron yuborish mantiqi
            def call_whisper_api():
                with open(self.temp_audio_file, "rb") as file:
                    transcription = self.groq_client.audio.transcriptions.create(
                        file=(self.temp_audio_file, file.read()),
                        model="whisper-large-v3",
                        language="uz",
                        response_format="text"
                    )
                return str(transcription).strip()

            response_text = await loop.run_in_executor(None, call_whisper_api)

            # Vaqtincha audio faylni o'chirish
            if os.path.exists(self.temp_audio_file):
                os.remove(self.temp_audio_file)
                
            return response_text

        except Exception:
            # Har qanday drayver yoki API ulanish uzilishida xatoni yutib, 
            # markaziy sikl aylanib ketishi uchun biroz kutib bo'sh matn qaytaramiz
            if os.path.exists(self.temp_audio_file):
                try: os.remove(self.temp_audio_file)
                except: pass
            await asyncio.sleep(1.0)
            return ""
def text_to_speech(text: str):
    """main.py uchun sinxron TTS wrapper"""
    if not text or not text.strip():
        return
    try:
        import edge_tts, asyncio, tempfile, os

        async def _speak():
            communicate = edge_tts.Communicate(text, voice="uz-UZ-SardorNeural")
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp = f.name
            await communicate.save(tmp)
            if os.name == "nt":
                os.system(f'start /min "" "{tmp}"')
            else:
                os.system(f"mpg123 '{tmp}' 2>/dev/null &")

        asyncio.run(_speak())
    except Exception:
        pass
