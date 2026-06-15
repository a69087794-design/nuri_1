import os
import asyncio
from groq import Groq

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
        """Matnni ovozga aylantirish (TTS) - WSL-xavfsiz"""
        if not text or not text.strip():
            return
        await asyncio.sleep(0.05)
        return

    async def listen_groq_whisper(self, duration: int = 4) -> str:
        """Mikrofondan ovozni asinxron yozib olib, Groq Whisper orqali matnga o'girish"""
        if not self.groq_client or not AUDIO_AVAILABLE:
            await asyncio.sleep(1.5)
            return ""

        fs = 16000
        try:
            loop = asyncio.get_event_loop()
            
            def record_audio():
                try:
                    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
                    sd.wait()
                    return recording
                except Exception:
                    return None

            recording = await loop.run_in_executor(None, record_audio)
            
            if recording is None:
                await asyncio.sleep(1.0)
                return ""

            wav.write(self.temp_audio_file, fs, recording)

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

            if os.path.exists(self.temp_audio_file):
                os.remove(self.temp_audio_file)
                
            return response_text

        except Exception:
            if os.path.exists(self.temp_audio_file):
                try: os.remove(self.temp_audio_file)
                except: pass
            await asyncio.sleep(1.0)
            return ""


def text_to_speech(text: str):
    """FIXED: Sinxron TTS wrapper - Thread-safe async management"""
    if not text or not text.strip():
        return
    try:
        import edge_tts
        import tempfile
        import threading
        
        async def _speak():
            try:
                communicate = edge_tts.Communicate(text, voice="uz-UZ-SardorNeural")
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    tmp = f.name
                await communicate.save(tmp)
                if os.name == "nt":
                    os.system(f'start /min "" "{tmp}"')
                else:
                    os.system(f"mpg123 '{tmp}' 2>/dev/null &")
            except Exception as e:
                print(f"[NURI.VOICE] TTS xatosi: {e}")
        
        # FIXED: Try existing event loop first, then create new one
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                thread = threading.Thread(target=lambda: asyncio.run(_speak()), daemon=True)
                thread.start()
            else:
                loop.run_until_complete(_speak())
        except RuntimeError:
            asyncio.run(_speak())
    except Exception as e:
        print(f"[NURI.VOICE] Edge-TTS qollashda xato: {e}")
