import os
import asyncio
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()

class TelegramModule:
    def __init__(self, core_processor=None):
        """NURI Telegram Automation Moduli"""
        
        self.core_processor = core_processor
        self.is_active = False
        self.use_adb = False
        self.use_gui = False
        
        # ADB orqali Android (DISPLAY kerak emas)
        if os.name != "nt":
            try:
                result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=2)
                if "device" in result.stdout and "offline" not in result.stdout:
                    self.use_adb = True
                    self.is_active = True
                    print("[NURI.TELEGRAM] Android ADB orqali Telegram boshqarilmoqda.")
            except Exception as e:
                print(f"[NURI.TELEGRAM] ADB topilmadi: {e}")
        
        # PyAutoGUI orqali Windows GUI (faqat Windows da)
        if not self.use_adb and os.name == "nt":
            try:
                import pyautogui
                self.use_gui = True
                self.is_active = True
                print("[NURI.TELEGRAM] Windows GUI orqali Telegram boshqarilmoqda.")
                pyautogui.FAILSAFE = True
            except Exception as e:
                print(f"[NURI.TELEGRAM] PyAutoGUI xatosi: {e}")
        
        if not self.is_active:
            print("[NURI.TELEGRAM] ADB yoki GUI topilmadi. Telegram o'chirildi.")

    def adb_tap(self, x: int, y: int):
        """Ekranga bosish (Android)"""
        try:
            subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], timeout=2)
            time.sleep(0.5)
        except Exception as e:
            print(f"[NURI.TELEGRAM] ADB tap xatosi: {e}")

    def adb_type(self, text: str):
        """Matn yozish (Android)"""
        try:
            escaped_text = text.replace("'", "\\'").replace('"', '\\"')
            subprocess.run(["adb", "shell", "input", "text", escaped_text], timeout=2)
            time.sleep(0.3)
        except Exception as e:
            print(f"[NURI.TELEGRAM] ADB type xatosi: {e}")

    def adb_swipe(self, x1: int, y1: int, x2: int, y2: int):
        """Ekranni swyipe qilish (Android)"""
        try:
            subprocess.run(
                ["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)],
                timeout=2
            )
            time.sleep(0.5)
        except Exception as e:
            print(f"[NURI.TELEGRAM] ADB swipe xatosi: {e}")

    async def send_message(self, chat_name: str, message: str):
        """Telegramda xabar yuborish"""
        if not self.is_active:
            print("[NURI.TELEGRAM] Telegram o'chirilgan.")
            return False

        try:
            if self.use_adb:
                subprocess.run(
                    ["adb", "shell", "am", "start", "-n", "org.telegram.messenger/.MainActivity"],
                    timeout=3
                )
                time.sleep(2)
                self.adb_tap(60, 60)
                time.sleep(1)
                self.adb_type(chat_name)
                time.sleep(1)
                self.adb_tap(540, 200)
                time.sleep(1)
                self.adb_tap(540, 900)
                time.sleep(0.5)
                self.adb_type(message)
                time.sleep(0.5)
                self.adb_tap(1050, 900)
                time.sleep(1)
                print(f"[NURI.TELEGRAM] Xabar yuborildi: {chat_name}")
                return True
            
            elif self.use_gui:
                import pyautogui
                pyautogui.click(100, 100)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'k')
                time.sleep(1)
                pyautogui.write(chat_name, interval=0.05)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.click(800, 700)
                time.sleep(0.5)
                pyautogui.write(message, interval=0.02)
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(1)
                print(f"[NURI.TELEGRAM] Xabar yuborildi: {chat_name}")
                return True
        except Exception as e:
            print(f"[NURI.TELEGRAM] Xabar yuborishda xatolik: {e}")
            return False

    async def open_chat(self, chat_name: str):
        """Chat-ni ochish"""
        if not self.is_active:
            return False

        try:
            if self.use_adb:
                subprocess.run(
                    ["adb", "shell", "am", "start", "-n", "org.telegram.messenger/.MainActivity"],
                    timeout=3
                )
                time.sleep(2)
                self.adb_tap(60, 60)
                time.sleep(1)
                self.adb_type(chat_name)
                time.sleep(1)
                self.adb_tap(540, 200)
                time.sleep(1)
                print(f"[NURI.TELEGRAM] Chat ochildi: {chat_name}")
                return True

            elif self.use_gui:
                import pyautogui
                pyautogui.click(100, 100)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'k')
                time.sleep(1)
                pyautogui.write(chat_name, interval=0.05)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                print(f"[NURI.TELEGRAM] Chat ochildi: {chat_name}")
                return True
        except Exception as e:
            print(f"[NURI.TELEGRAM] Chat ochishda xatolik: {e}")
            return False

    async def read_messages(self):
        """Ekrandagi habarlarni o'qish"""
        if not self.is_active:
            return []

        try:
            if self.use_adb:
                result = subprocess.run(
                    ["adb", "shell", "dumpsys", "accessibility"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                return result.stdout.split('\n')[:20]
            elif self.use_gui:
                print("[NURI.TELEGRAM] GUI dan habar o'qish hozir qo'llanma.")
                return []
        except Exception as e:
            print(f"[NURI.TELEGRAM] Habar o'qishda xatolik: {e}")
            return []

    async def scroll_up(self):
        """Chat-da yuqoriga scroll qilish"""
        try:
            if self.use_adb:
                self.adb_swipe(540, 300, 540, 700)
                print("[NURI.TELEGRAM] Yuqoriga scroll qilindi.")
            elif self.use_gui:
                import pyautogui
                pyautogui.scroll(5)
                print("[NURI.TELEGRAM] Yuqoriga scroll qilindi.")
        except Exception as e:
            print(f"[NURI.TELEGRAM] Scroll xatosi: {e}")

    async def start_listening(self):
        """Telegram automation fonda tinglamoq"""
        if self.is_active:
            print("[NURI.TELEGRAM] Automation fonda ishga tushdi.")
