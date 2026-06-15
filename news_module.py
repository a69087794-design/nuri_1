import os

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_KEY = os.getenv("GROQ_API_KEY_1")
    groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
    GROQ_AVAILABLE = bool(groq_client)
except Exception:
    GROQ_AVAILABLE = False
    groq_client = None

NEWS_SOURCES = {
    "dunyo":      "https://feeds.bbcnews.com/rss/world",
    "texnologiya":"https://feeds.feedburner.com/TechCrunch",
    "o'zbekiston":"https://kun.uz/rss",
    "sport":      "https://feeds.bbcnews.com/rss/sport",
    "iqtisodiyot":"https://feeds.bbcnews.com/rss/business",
}

def can_handle(text: str) -> bool:
    return "yangilik" in text.lower() or "xabar" in text.lower()

def get_news(topic: str = "dunyo", limit: int = 5) -> str:
    if not FEEDPARSER_AVAILABLE:
        return "feedparser o'rnatilmagan. pip install feedparser"
    url = NEWS_SOURCES.get(topic.lower(), NEWS_SOURCES["dunyo"])
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            return "Yangiliklar topilmadi."
        result = f"So'nggi {topic} yangiliklari:\n\n"
        for i, entry in enumerate(feed.entries[:limit]):
            result += f"{i+1}. {entry.title}\n"
            if hasattr(entry, 'summary'):
                result += f"   {entry.summary[:120]}...\n\n"
        return result
    except Exception as e:
        return f"Xato: {e}"

def process_command(text: str) -> str:
    lower = text.lower()
    if "texnologiya" in lower:
        return get_news("texnologiya")
    elif "sport" in lower:
        return get_news("sport")
    elif "iqtisodiyot" in lower:
        return get_news("iqtisodiyot")
    elif "o'zbekiston" in lower or "uzbekiston" in lower:
        return get_news("o'zbekiston")
    else:
        return get_news("dunyo")
