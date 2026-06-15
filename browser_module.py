import os
import subprocess
import webbrowser

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

driver = None

def open_browser(url: str = "https://google.com") -> str:
    try:
        webbrowser.open(url)
        return f"Brauzer ochildi: {url}"
    except Exception as e:
        return f"Xato: {e}"

def start_selenium() -> str:
    global driver
    if not SELENIUM_AVAILABLE:
        return "Selenium hozircha ishlamayapti."
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return "Brauzer ishga tushdi."
    except Exception as e:
        return f"Xato: {e}"

def search_google(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Google da qidirилdi: {query}"
    except Exception as e:
        return f"Xato: {e}"

def search_youtube(query: str) -> str:
    try:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"YouTube da qidirилdi: {query}"
    except Exception as e:
        return f"Xato: {e}"

def open_url(url: str) -> str:
    try:
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Ochildi: {url}"
    except Exception as e:
        return f"Xato: {e}"

def close_browser() -> str:
    global driver
    if driver:
        try:
            driver.quit()
            driver = None
            return "Brauzer yopildi."
        except Exception as e:
            return f"Xato: {e}"
    return "Brauzer ochiq emas."

def process_browser_command(text: str) -> str:
    text_lower = text.lower()

    # Google qidirish
    if "google da qidir" in text_lower or "googledan qidir" in text_lower:
        query = text.split("qidir", 1)[1].strip()
        return search_google(query)

    # YouTube qidirish
    elif "youtube da qidir" in text_lower or "youtubedan qidir" in text_lower:
        query = text.split("qidir", 1)[1].strip()
        return search_youtube(query)

    # YouTube ochish
    elif "youtube" in text_lower and "och" in text_lower:
        return open_url("https://youtube.com")

    # Google ochish
    elif "google" in text_lower and "och" in text_lower:
        return open_url("https://google.com")

    # Brauzer ochish
    elif "brauzer" in text_lower and "och" in text_lower:
        return open_browser()

    # Brauzer yopish
    elif "brauzer" in text_lower and "yop" in text_lower:
        return close_browser()

    # URL ochish
    elif "och " in text_lower and ("http" in text_lower or "www" in text_lower or ".com" in text_lower):
        parts = text.split("och ", 1)
        if len(parts) > 1:
            return open_url(parts[1].strip())

    return "Brauzer buyrug'i tushunilmadi."
