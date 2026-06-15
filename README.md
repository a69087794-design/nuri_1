# NURI - Neyronli Universal Robot Intellekti

Advanced AI assistant application with GUI, voice capabilities, and Telegram integration.

## 📋 Talab qilinadigan Resurslar
- Windows 7+ / macOS / Linux
- Python 3.9+
- Minimal 2GB RAM
- Internet ulanishi

## 🚀 EXE Faylni Yaratish

### 1. **Paketlarni O'rnatish**
```bash
pip install -r requirements.txt
```

### 2. **EXE Faylni Yaratish**

**Windows:**
```bash
build.bat
```

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

Yoki to'g'ridan-to'g'ri Python orqali:
```bash
python build_exe.py
```

Shuni 5-10 daqiqa vaqt oladi. Tayyorlanganda:
- `dist/NURI.exe` - Standalone executable (Windows)
- `dist/NURI` - Standalone executable (Linux/macOS)

### 3. **Ishga Tushirish**
```bash
dist/NURI.exe  # Windows
./dist/NURI    # Linux/macOS
```

## ⚙️ Konfiguratsiya

`.env` faylini yarating va qo'shish:

```env
ADMIN_PASSWORD=darling
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🎯 Asosiy Xususiyatlar

- **GUI Interface** - Modern PyQt5 interfeysi
- **Voice Support** - Edge-TTS bilan text-to-speech
- **AI Engine** - Groq API orqali
- **Telegram Bot** - Xabar yuborish va qabul qilish
- **Memory System** - Suhbat tarixi saqlash
- **Plugin System** - Kengaytmalar qo'shish
- **Multi-user** - Admin va user rollari

## 📁 Fayllar Tuzilishi

```
nuri_darling/
├── main.py              # CLI entry point
├── gui.py              # GUI entry point
├── ai_engine.py        # AI asosiy tizim
├── voice_engine.py     # Ovoz qayta ishlash
├── telegram_module.py  # Telegram integratsiyasi
├── memory_module.py    # Suhbat xotirasini saqlash
├── identity_engine.py  # Foydalanuvchi autentifikatsiyasi
├── browser_module.py   # Brauzer avtomatsiyasi
├── emotion_module.py   # Emosyon aniqlash
├── keyboard_module.py  # Klavier kiritish
├── security_module.py  # Xavfsizlik funksiyalari
├── permissions.py      # Ruxsatnomalar
├── strategy_module.py  # Strategiya tizimi
├── network_module.py   # Tarmoq operatsiyalari
├── news_module.py      # Yangiliklar modulisi
├── youtube_module.py   # YouTube integratsiyasi
├── vision_module.py    # Koʻrish/rasm qayta ishlash
├── build_exe.py        # EXE yaratish skripti (Python)
├── build.bat           # EXE yaratish (Windows)
├── build.sh            # EXE yaratish (Linux/macOS)
├── setup.py            # Paketni o'rnatish
├── requirements.txt    # Kerakli paketlar
└── README.md           # Bu fayl

plugins/                # Foydalanuvchi pluginlari
```

## 🔐 Xavfsizlik

- Default admin paroli: `darling`
- Parolni `.env` faylida o'zgartiring
- Identifikatsiya ma'lumotlari SQLite bazasida saqlanadi

## 🛠️ Muammoni Hal Qilish

**PyInstaller xatosi?**
```bash
pip install --upgrade pyinstaller
```

**API kalitlari kerak?**
- [Groq API](https://console.groq.com)
- [Google Gemini API](https://makersuite.google.com/app/apikey)
- [Telegram Bot](https://t.me/botfather)

**EXE ochilmayapti?**
- `.env` faylini tekshiring
- API kalitlarini tekshiring
- Antivirus/Windows Defender chekni qo'ying

## 📝 Lisenziya

MIT License

## 👨‍💻 Muallif

horaphile

---

**Ishlang va o'zingizsni taanniytirish uchun!"** 🚀
