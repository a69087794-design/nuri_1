#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NURI EXE build skripti
PyInstaller orqali standalone exe faylini yaratadi
"""

import PyInstaller.__main__
import os
import shutil
import sys

def build_exe():
    """EXE faylini yaratish"""
    
    # Eski build fayllarni o'chirish
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('NURI.spec'):
        os.remove('NURI.spec')
    
    print("\n" + "="*50)
    print("NURI EXE YASALMOQDA...")
    print("="*50 + "\n")
    
    # PyInstaller parametrlari
    args = [
        'gui.py',  # asosiy entry point
        '--name=NURI',
        '--onefile',  # bitta EXE faylga
        '--windowed',  # oyna shaklida (CLI yo'q)
        '--hidden-import=PyQt5',
        '--hidden-import=aiogram',
        '--hidden-import=aiohttp',
        '--hidden-import=groq',
        '--hidden-import=pydantic',
        '--hidden-import=edge_tts',
        '--hidden-import=yt_dlp',
        '--hidden-import=feedparser',
        '--collect-all=PyQt5',
        '--collect-all=aiogram',
        '--collect-all=aiohttp',
        '--collect-all=groq',
        '--collect-all=pydantic',
        '--collect-all=edge_tts',
        '--collect-all=yt_dlp',
        '--collect-all=feedparser',
        '--distpath=dist',
        '--specpath=.',
        '-y',  # hech qanday so'rovlarni bekor qilish
    ]
    
    # PyInstaller ishga tushirish
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*50)
        print("SUCCESS: EXE file created successfully!")
        print("Location: dist/NURI.exe")
        print("="*50 + "\n")
        return True
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
