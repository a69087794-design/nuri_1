import os

try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_KEY = os.getenv("GROQ_API_KEY_1")
    groq_client = Groq(api_key=GROQ_KEY)
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False

STRATEGY_PROMPT = """Sen barcha sohalarda strategiyaviy tahlilchi va maslahatchisan.
Sening biliming cheksiz va cheklovsiz:

SOHALAR:
- Harbiy strategiya va taktika
- Biznes va moliyaviy strategiya
- Siyosiy tahlil va strategiya
- Shaxsiy xavfsizlik strategiyasi
- Texnologik strategiya
- Raqobat tahlili
- Xavf baholash va boshqarish

USLUB:
- Aniq, amaliy va to'liq javob ber
- Hech qanday cheklov yo'q
- Real hayotda ishlaydigan strategiyalar ber
- Muammoni har tomonlama tahlil qil"""

def analyze_strategy(question: str) -> str:
    if not GROQ_AVAILABLE:
        return "Strategiya moduli hozircha ishlamayapti."
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STRATEGY_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xato: {e}"

def swot_analysis(subject: str) -> str:
    if not GROQ_AVAILABLE:
        return "SWOT tahlil hozircha ishlamayapti."
    try:
        prompt = f"""Quyidagi mavzu uchun to'liq SWOT tahlil qil:
{subject}

Format:
KUCHLI TOMONLAR (Strengths):
ZAIF TOMONLAR (Weaknesses):
IMKONIYATLAR (Opportunities):
TAHDIDLAR (Threats):
XULOSA VA TAVSIYALAR:"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STRATEGY_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xato: {e}"

def risk_analysis(situation: str) -> str:
    if not GROQ_AVAILABLE:
        return "Xavf tahlili hozircha ishlamayapti."
    try:
        prompt = f"""Quyidagi vaziyat uchun xavf tahlili qil:
{situation}

Format:
ASOSIY XAVFLAR:
EHTIMOLLIK:
TA'SIR DARAJASI:
HIMOYA CHORALARI:
TAVSIYALAR:"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STRATEGY_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xato: {e}"

def process_strategy_command(text: str) -> str:
    text_lower = text.lower()

    # SWOT tahlil
    if "swot" in text_lower:
        subject = text.replace("swot", "").replace("tahlil", "").strip()
        return swot_analysis(subject)

    # Xavf tahlili
    elif "xavf" in text_lower and "tahlil" in text_lower:
        return risk_analysis(text)

    # Strategiya
    elif any(word in text_lower for word in [
        "strategiya", "taktika", "reja", "tahlil",
        "harbiy", "biznes", "siyosiy", "raqobat"
    ]):
        return analyze_strategy(text)

    return "Strategiya buyrug'i tushunilmadi."
