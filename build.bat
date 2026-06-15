@echo off
REM NURI EXE Build Skripti (Windows)
REM PyInstaller orqali standalone exe faylini yaratadi

echo.
echo ============================================================
echo NURI EXE YASALMOQDA (Windows)...
echo ============================================================
echo.

REM Eski build fayllarni o'chirish
if exist dist (
    echo [*] dist folder o'chirilmoqda...
    rmdir /s /q dist
)
if exist build (
    echo [*] build folder o'chirilmoqda...
    rmdir /s /q build
)
if exist NURI.spec (
    echo [*] NURI.spec o'chirilmoqda...
    del NURI.spec
)

echo [*] Paketlar o'rnatilmoqda...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo [*] PyInstaller ishga tushirilmoqda...
python -m PyInstaller gui.py --name=NURI --onefile --windowed ^
    --hidden-import=PyQt5 ^
    --hidden-import=aiogram ^
    --hidden-import=aiohttp ^
    --hidden-import=groq ^
    --hidden-import=pydantic ^
    --hidden-import=edge_tts ^
    --hidden-import=yt_dlp ^
    --hidden-import=feedparser ^
    --collect-all=PyQt5 ^
    --collect-all=aiogram ^
    --collect-all=aiohttp ^
    --collect-all=groq ^
    --collect-all=pydantic ^
    --collect-all=edge_tts ^
    --collect-all=yt_dlp ^
    --collect-all=feedparser ^
    --distpath=dist ^
    --specpath=. ^
    -y

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS: NURI.exe yaratildi!
    echo Location: dist\NURI.exe
    echo ============================================================
    echo.
    pause
) else (
    echo.
    echo ============================================================
    echo ERROR: Build jarayoni muvaffaqiyatsiz bo'ldi!
    echo ============================================================
    echo.
    pause
    exit /b 1
)
