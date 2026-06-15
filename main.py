import os
import sys
import asyncio
import getpass
import importlib.util
import logging
import concurrent.futures
import aiohttp
from dotenv import load_dotenv

load_dotenv()

from ai_engine import AIEngine
from keyboard_module import KeyboardModule
from telegram_module import TelegramModule
import voice_engine as ve
import identity_engine as ie
import memory_module as mm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NURICore:
    def __init__(self):
        print("\n[NURI.SYSTEM] Ishga tushmoqda...")
        mm.init_db()
        ie.setup_identity()
        self.ai = AIEngine()
        self.keyboard = KeyboardModule()
        self.telegram = TelegramModule(core_processor=self._process_command_sync)
        self.current_user = "stranger"
        self.current_role = "stranger"
        self.plugins = {}
        self._load_plugins()
        self.max_context_tokens = 1500
        print("[NURI.SYSTEM] Tayyor ✅\n")

    def _load_plugins(self):
        base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
        plugins_dir = os.path.join(base_path, "plugins")
        os.makedirs(plugins_dir, exist_ok=True)
        for filename in sorted(os.listdir(plugins_dir)):
            if filename.endswith(".py") and not filename.startswith("_"):
                try:
                    spec = importlib.util.spec_from_file_location(filename[:-3], os.path.join(plugins_dir, filename))
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.plugins[filename[:-3]] = module
                        print(f"[NURI] ✅ {filename[:-3]}")
                except Exception as e:
                    logger.error(f"Plugin {filename}: {e}")

    async def speak_and_print(self, text: str):
        if text and text.strip():
            print(f"\n[NURI]: {text}")
            try:
                await asyncio.wait_for(asyncio.get_event_loop().run_in_executor(None, ve.text_to_speech, text), timeout=5.0)
            except Exception:
                pass

    async def check_apis(self):
        print("\n" + "="*40 + "\nAPI CHECK\n" + "="*40)
        async with aiohttp.ClientSession() as session:
            for name, url in [("Groq", "https://api.groq.com/openai/v1/models"), ("Gemini", "https://generativelanguage.googleapis.com/v1beta/models")]:
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                        print(f"  ✅ {name}" if r.status in (200, 401, 403) else f"  ❌ {name}")
                except:
                    print(f"  ❌ {name}")
        print("="*40 + "\n")

    async def authenticate_startup(self) -> bool:
        print("\n" + "="*40 + "\n  NURI\n" + "="*40 + "\n")
        await self.check_apis()
        admin_pass = os.getenv("ADMIN_PASSWORD", "darling")
        while True:
            try:
                password = getpass.getpass("Parol → ")
            except (KeyboardInterrupt, EOFError):
                return False
            if password == admin_pass:
                self.current_role, self.current_user = "admin", "admin"
                await self.speak_and_print("Admin sifatida kirdingiz!")
                return True
            elif ie.verify_user_password(password):
                self.current_role, self.current_user = "user", ie.get_username_by_password(password) or "user"
                await self.speak_and_print(f"Xush kelibsiz, {self.current_user}!")
                return True
            else:
                print("[NURI] Parol xato.\n")

    def _process_command_sync(self, command: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                future = asyncio.run_coroutine_threadsafe(self.process_command(command), loop)
                return future.result(timeout=45)
            return loop.run_until_complete(self.process_command(command))
        except concurrent.futures.TimeoutError:
            return "Vaqt tugadi."
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return f"Xatolik: {str(e)[:80]}"

    async def process_command(self, command: str) -> str:
        if not command or not command.strip():
            return ""
        cmd, lower = command.strip(), command.strip().lower()
        
        if lower.startswith(("admin:", "user:")):
            prefix, password = lower.split(":", 1)[0], cmd.split(":", 1)[1].strip()
            if prefix == "admin" and password == os.getenv("ADMIN_PASSWORD", "darling"):
                self.current_role, self.current_user = "admin", "admin"
                msg = "Admin sifatida qayta kirdingiz!"
                mm.save_conversation("admin", cmd, msg)
                await self.speak_and_print(msg)
                return msg
            elif prefix == "user" and ie.verify_user_password(password):
                self.current_user = ie.get_username_by_password(password) or "user"
                self.current_role = "user"
                msg = f"User sifatida kirdingiz ({self.current_user})!"
                mm.save_conversation(self.current_user, cmd, msg)
                await self.speak_and_print(msg)
                return msg
            return "Parol xato!"
        
        if self.current_role == "stranger":
            return "Avval parol kiriting!"
        
        if self.current_role == "admin":
            if any(kw in lower for kw in ["status", "holat"]):
                ai_status = await self.ai.get_status()
                response = f"NURI STATUS\nFoydalanuvchi: {self.current_user}\nAI Engines: {ai_status['total_engines']}\nPlugins: {len(self.plugins)}"
                mm.save_conversation(self.current_user, cmd, response)
                await self.speak_and_print(response)
                return response
            if "plugin" in lower and "qayta yukla" in lower:
                self.plugins.clear()
                self._load_plugins()
                await self.speak_and_print("Plugins qayta yuklandi")
                return "OK"
            if "telegram" in lower:
                return await self._handle_telegram(cmd, lower)
        
        if self.current_role == "user" and any(kw in lower for kw in ["telegram", "parol"]):
            return "Admin uchun!"
        
        for plugin_name, plugin in self.plugins.items():
            try:
                if hasattr(plugin, 'can_handle') and plugin.can_handle(lower):
                    if hasattr(plugin, 'process_command'):
                        result = plugin.process_command(cmd)
                        if result:
                            mm.save_conversation(self.current_user, cmd, result)
                            await self.speak_and_print(result)
                            return result
            except Exception as e:
                logger.error(f"Plugin {plugin_name}: {e}")
                continue
        
        try:
            history = mm.get_history(self.current_user, limit=5) or ""
            if len(history) > 2000:
                history = history[-2000:]
            full_prompt = f"{history}\nFoydalanuvchi: {cmd}" if history else cmd
            ai_response = await asyncio.wait_for(self.ai.generate_response(full_prompt), timeout=35.0)
            result = ai_response if ai_response else "Bo'sh javob"
            mm.save_conversation(self.current_user, cmd, result)
            await self.speak_and_print(result)
            return result
        except asyncio.TimeoutError:
            msg = "AI vaqti tugadi (35s)"
            mm.save_conversation(self.current_user, cmd, msg)
            return msg
        except Exception as e:
            msg = f"AI xatosi: {str(e)[:80]}"
            mm.save_conversation(self.current_user, cmd, msg)
            return msg

    async def _handle_telegram(self, cmd: str, lower: str) -> str:
        if not self.telegram.is_active:
            return "Telegram moduli faol emas."
        try:
            if "xabar yubor" in lower:
                after_parts = cmd.lower().split("xabar yubor", 1)
                if len(after_parts) < 2:
                    return "Format: telegram xabar yubor @chat ga Xabar"
                ga_parts = after_parts[1].strip().split(" ga ", 1)
                if len(ga_parts) != 2 or not ga_parts[0].strip() or not ga_parts[1].strip():
                    return "Format: telegram xabar yubor @chat ga Xabar"
                chat, message = ga_parts
                try:
                    result = await self.telegram.send_message(chat.strip(), message.strip())
                    response = "Xabar yuborildi!" if result else "Xabar yuborilmadi."
                except Exception as e:
                    logger.error(f"Telegram send: {e}")
                    response = "Telegram xatosi."
            elif "chat och" in lower:
                chat_name = cmd.lower().replace("telegram chat och", "").strip()
                response = "Chat ochildi!" if chat_name and await self.telegram.open_chat(chat_name) else "Chat nomi kerak."
            elif any(w in lower for w in ["o'qi", "oqi"]):
                messages = await self.telegram.read_messages()
                response = ("Habarlar:\n" + "\n".join(messages[:10])) if messages else "Habar topilmadi."
            elif "scroll" in lower:
                await self.telegram.scroll_up()
                response = "Scroll qilindi."
            else:
                response = "Telegram: xabar yubor | chat och | o'qi | scroll"
            mm.save_conversation(self.current_user, cmd, response)
            return response
        except Exception as e:
            logger.error(f"Telegram: {e}")
            return "Telegram xatosi."

    async def start_loop(self):
        if self.telegram.is_active:
            asyncio.create_task(self.telegram.start_listening())
        await self.speak_and_print("NURI tayyor!")
        print("\n" + "="*40 + "\nBUYRUQLAR\nstatus, plugin qayta yukla, chiqish\n" + "="*40 + "\n")
        loop = asyncio.get_event_loop()
        while True:
            try:
                cmd = await loop.run_in_executor(None, input, "[→] ")
                if cmd.strip().lower() in ("chiqish", "exit", "quit"):
                    await self.speak_and_print("Xayr!")
                    break
                await self.process_command(cmd.strip())
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Loop: {e}")
                await asyncio.sleep(1)

async def main():
    nuri = NURICore()
    if await nuri.authenticate_startup():
        await nuri.start_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nYakunlandi.")
