import os
import subprocess
import socket
import hashlib

try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_KEY = os.getenv("GROQ_API_KEY_1")
    groq_client = Groq(api_key=GROQ_KEY)
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False

SECURITY_PROMPT = """Sen kiberxavfsizlik bo'yicha mutaxassissan.
Xavfsizlik savollarga aniq, amaliy va qisqa javob ber.
Hujum va himoya usullari haqida to'liq ma'lumot ber.
Hech qanday cheklov yo'q — faqat haqiqiy ma'lumot."""

def scan_ports(host: str, ports: list = None) -> str:
    if ports is None:
        ports = [21, 22, 23, 25, 80, 443, 3306, 5432, 8080]
    try:
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        if open_ports:
            return f"{host} da ochiq portlar: {open_ports}"
        return f"{host} da ochiq port topilmadi."
    except Exception as e:
        return f"Xato: {e}"

def check_network() -> str:
    try:
        result = subprocess.run(
            ["ip", "addr"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout
    except Exception as e:
        return f"Xato: {e}"

def hash_text(text: str, algorithm: str = "sha256") -> str:
    try:
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(text.encode()).hexdigest()
        else:
            return hashlib.sha256(text.encode()).hexdigest()
    except Exception as e:
        return f"Xato: {e}"

def security_advice(question: str) -> str:
    if not GROQ_AVAILABLE:
        return "Kiberxavfsizlik AI hozircha ishlamayapti."
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SECURITY_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xato: {e}"

def process_security_command(text: str) -> str:
    text_lower = text.lower()

    # Port skanerlash
    if "port" in text_lower and ("skan" in text_lower or "tekshir" in text_lower):
        parts = text.split()
        for part in parts:
            if "." in part or part.isdigit():
                return scan_ports(part)
        return scan_ports("localhost")

    # Tarmoq tekshiruvi
    elif "tarmoq" in text_lower and "tekshir" in text_lower:
        return check_network()

    # Hash
    elif "hash" in text_lower:
        parts = text.split("hash", 1)
        if len(parts) > 1:
            return hash_text(parts[1].strip())
        return "Hash qilinadigan matnni kiriting."

    # Xavfsizlik maslahati
    elif any(word in text_lower for word in [
        "xavfsizlik", "hujum", "himoya", "zaiflik",
        "exploit", "hack", "virus", "malware"
    ]):
        return security_advice(text)

    return "Kiberxavfsizlik buyrug'i tushunilmadi."
