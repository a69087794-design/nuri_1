import os
import time

# PyAutoGUI importini xavfsiz blok ichiga olamiz
try:
    import pyautogui
    # Agar DISPLAY o'zgaruvchisi o'rnatilmagan bo'lsa, Linuxda pyautogui ishga tushmaydi
    if "DISPLAY" not in os.environ and os.name != "nt":
        raise KeyError("DISPLAY topilmadi")
    GUI_AVAILABLE = True
except Exception:
    GUI_AVAILABLE = False

class KeyboardModule:
    def __init__(self):
        if GUI_AVAILABLE:
            print("[NURI.KEYBOARD] Klaviatura va tizim avtomatizatsiyasi faol (GUI).")
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
        else:
            print("[NURI.KEYBOARD] [DIQQAT] Ekran (DISPLAY) aniqlanmadi. "
                  "Klaviatura boshqaruvi o'chirildi, CLI rejimida davom etamiz.")

    def is_available(self) -> bool:
            return GUI_AVAILABLE
    def execute_action(self, command: str) -> str:
        """
        Buyruqni tahlil qiladi. Agar GUI ishlamayotgan bo'lsa, 
        foydalanuvchiga faqat Windowsda ishlashini ma'lum qiladi.
        """
        command = command.strip().lower()

        # Agar X-Server yoki Ekran ulanmagan bo'lsa, xavfsiz rad etish
        if not GUI_AVAILABLE:
            return ("Kechirasiz, klaviatura va tizim harakatlarini boshqarish "
                    "faqat grafik ekran (Windows/GUI) rejimida ishlaydi. "
                    "Hozirda CLI rejimida faqat suhbatlashishimiz mumkin.")

        # ---- AGAR GUI MAVJUD BO'LSA, ASOSIY MANTIQ ----
        
        # 1. Skrinshot olish
        if "skrinshot" in command or "ekranni rasmga ol" in command:
            try:
                os.makedirs("screenshots", exist_ok=True)
                filename = f"screenshots/screenshot_{int(time.time())}.png"
                pyautogui.screenshot(filename)
                return f"Ekran rasmga olindi: {filename}"
            except Exception as e:
                return f"Skrinshotda xatolik: {e}"

        # 2. Matn yozish
        elif "yoz" in command:
            text_to_write = command.split("yoz", 1)[1].strip()
            if not text_to_write:
                return "Nima deb yozishni tushunmadim."
            try:
                pyautogui.write(text_to_write, interval=0.1)
                return f"Yozildi: '{text_to_write}'"
            except Exception as e:
                return f"Xatolik: {e}"

        # 3. Tugmalarni bosish
        elif "bos" in command:
            if "enter" in command:
                pyautogui.press("enter")
                return "Enter bosildi."
            elif "space" in command or "probel" in command:
                pyautogui.press("space")
                return "Probel bosildi."
            else:
                return "Tugma tushunarsiz."

        return "Klaviatura modulida ushbu buyruq uchun ishlamaydi."
