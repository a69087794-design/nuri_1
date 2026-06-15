import os
import subprocess
import webbrowser

try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False

def search_youtube(query: str) -> str:
    try:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"YouTube da qidirилdi: {query}"
    except Exception as e:
        return f"Xato: {e}"

def play_youtube(query: str) -> str:
    try:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"YouTube da ijro etilmoqda: {query}"
    except Exception as e:
        return f"Xato: {e}"

def download_youtube(url: str, path: str = None) -> str:
    if not YTDLP_AVAILABLE:
        return "YouTube yuklab olish hozircha ishlamayapti."
    if path is None:
        path = os.path.expanduser("~/nuri/downloads")
    try:
        os.makedirs(path, exist_ok=True)
        ydl_opts = {
            "outtmpl": f"{path}/%(title)s.%(ext)s",
            "format": "best",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Yuklab olindi: {path}"
    except Exception as e:
        return f"Xato: {e}"

def download_audio(url: str, path: str = None) -> str:
    if not YTDLP_AVAILABLE:
        return "Audio yuklab olish hozircha ishlamayapti."
    if path is None:
        path = os.path.expanduser("~/nuri/downloads")
    try:
        os.makedirs(path, exist_ok=True)
        ydl_opts = {
            "outtmpl": f"{path}/%(title)s.%(ext)s",
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Audio yuklab olindi: {path}"
    except Exception as e:
        return f"Xato: {e}"

def process_youtube_command(text: str) -> str:
    text_lower = text.lower()

    # Qidirish
    if "youtube" in text_lower and "qidir" in text_lower:
        query = text.split("qidir", 1)[1].strip()
        return search_youtube(query)

    # Ijro etish
    elif "youtube" in text_lower and ("ijro" in text_lower or "ko'rsat" in text_lower or "och" in text_lower):
        query = text.split("youtube", 1)[1].strip()
        if "ijro" in query:
            query = query.split("ijro", 1)[1].strip()
        elif "ko'rsat" in query:
            query = query.split("ko'rsat", 1)[1].strip()
        return play_youtube(query)

    # Video yuklab olish
    elif "yuklab ol" in text_lower and "youtube" in text_lower:
        parts = text.split("yuklab ol", 1)
        if len(parts) > 1:
            url = parts[1].strip()
            return download_youtube(url)
        return "YouTube URL ni kiriting."

    # Audio yuklab olish
    elif "mp3" in text_lower or "audio" in text_lower:
        parts = text.split()
        for part in parts:
            if "youtube.com" in part or "youtu.be" in part:
                return download_audio(part)
        return "YouTube URL ni kiriting."

    return "YouTube buyrug'i tushunilmadi."
