import sqlite3
import os

DB_PATH = os.path.expanduser("~/nuri/nuri.db")

def _get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    """SQLite jadvallarini yaratish"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT    NOT NULL DEFAULT 'user',
                timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT    NOT NULL,
                ai_response  TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
    print("[NURI.MEMORY] SQLite xotira bazasi yuklandi ✅")

def save_conversation(username: str, user_msg: str, ai_msg: str):
    """Suhbatni saqlash"""
    if not user_msg or not ai_msg:
        return
    try:
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO chat_history (username, user_message, ai_response) VALUES (?, ?, ?)",
                (username or "user", user_msg.strip(), ai_msg.strip())
            )
            conn.commit()
    except Exception as e:
        print(f"[NURI.MEMORY] Saqlash xatosi: {e}")

def get_history(username: str, limit: int = 5) -> str:
    """Oxirgi N ta suhbatni kontekst sifatida qaytarish"""
    try:
        with _get_conn() as conn:
            cursor = conn.execute(
                "SELECT user_message, ai_response FROM chat_history WHERE username=? ORDER BY id DESC LIMIT ?",
                (username or "user", limit)
            )
            rows = cursor.fetchall()

        if not rows:
            return ""

        rows.reverse()
        history = "Oldingi muloqot:\n"
        for u, a in rows:
            history += f"Foydalanuvchi: {u}\nNURI: {a}\n"
        return history

    except Exception as e:
        print(f"[NURI.MEMORY] Tarix xatosi: {e}")
        return ""

def save_setting(key: str, value: str):
    """Sozlamani saqlash"""
    try:
        with _get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)",
                (key, value)
            )
            conn.commit()
    except Exception as e:
        print(f"[NURI.MEMORY] Sozlama xatosi: {e}")

def get_setting(key: str, default: str = "") -> str:
    """Sozlamani olish"""
    try:
        with _get_conn() as conn:
            cursor = conn.execute(
                "SELECT value FROM system_config WHERE key=?", (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else default
    except Exception:
        return default

def clear_memory(username: str = None) -> str:
    """Xotirani tozalash"""
    try:
        with _get_conn() as conn:
            if username:
                conn.execute("DELETE FROM chat_history WHERE username=?", (username,))
            else:
                conn.execute("DELETE FROM chat_history")
            conn.commit()
        return "Xotira tozalandi ✅"
    except Exception as e:
        return f"Xotirani tozalashda xatolik: {e}"
