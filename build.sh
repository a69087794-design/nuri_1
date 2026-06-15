#!/bin/bash
# NURI EXE Build Skripti (Linux/macOS)
# PyInstaller orqali standalone faylini yaratadi

echo ""
echo "=========================================================="
echo "NURI EXE YASALMOQDA (Linux/macOS)..."
echo "=========================================================="
echo ""

# Eski build fayllarni o'chirish
if [ -d "dist" ]; then
    echo "[*] dist folder o'chirilmoqda..."
    rm -rf dist
fi

if [ -d "build" ]; then
    echo "[*] build folder o'chirilmoqda..."
    rm -rf build
fi

if [ -f "NURI.spec" ]; then
    echo "[*] NURI.spec o'chirilmoqda..."
    rm NURI.spec
fi

echo "[*] Paketlar o'rnatilmoqda..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "[*] PyInstaller ishga tushirilmoqda..."
python -m PyInstaller gui.py --name=NURI --onefile \
    --hidden-import=PyQt5 \
    --hidden-import=aiogram \
    --hidden-import=aiohttp \
    --hidden-import=groq \
    --hidden-import=pydantic \
    --hidden-import=edge_tts \
    --hidden-import=yt_dlp \
    --hidden-import=feedparser \
    --collect-all=PyQt5 \
    --collect-all=aiogram \
    --collect-all=aiohttp \
    --collect-all=groq \
    --collect-all=pydantic \
    --collect-all=edge_tts \
    --collect-all=yt_dlp \
    --collect-all=feedparser \
    --distpath=dist \
    --specpath=. \
    -y

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================================="
    echo "SUCCESS: NURI executable yaratildi!"
    echo "Location: dist/NURI"
    echo "=========================================================="
    echo ""
    chmod +x dist/NURI
else
    echo ""
    echo "=========================================================="
    echo "ERROR: Build jarayoni muvaffaqiyatsiz bo'ldi!"
    echo "=========================================================="
    echo ""
    exit 1
fi
