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

EMOTION_PROMPT = """Sen foydalanuvchi ovozi va matnidan hissiyotni aniqlaydigan mutaxassissan.
Quyidagi hissiyotlarni aniqla:
- Xursand, g'amgin, g'azablangan, qo'rqqan, hayron, bezovta, tinch

Foydalanuvchi matnini tahlil qilib:
1. Asosiy hissiyotni aniqla
2. Hissiyot darajasini (past/o'rta/yuqori) ko'rsat
3. NURI qanday munosabat ko'rsatishi kerakligini tavsiya et"""

def detect_emotion(text: str) -> dict:
    if not GROQ_AVAILABLE:
        return {"emotion": "noaniq", "level": "o'rta", "advice": ""}
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": EMOTION_PROMPT},
                {
                    "role": "user",
                    "content": f"Quyidagi matndan hissiyotni aniqla:\n{text}"
                }
            ],
            max_tokens=200
        )
        result = response.choices[0].message.content
        return {"emotion": result, "level": "o'rta", "advice": result}
    except Exception as e:
        return {"emotion": "noaniq", "level": "o'rta", "advice": str(e)}

def adapt_response(text: str, response: str) -> str:
    if not GROQ_AVAILABLE:
        return response
    try:
        emotion_data = detect_emotion(text)
        emotion = emotion_data.get("emotion", "")

        prompt = f"""Foydalanuvchi hissiyoti: {emotion}
Asl javob: {response}

Javobni foydalanuvchi hissiyotiga mos ravishda qayta yoz.
Qisqa va tabiiy bo'lsin."""

        adapted = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return adapted.choices[0].message.content
    except Exception:
        return response

def get_emotion_response(emotion: str) -> str:
    responses = {
        "xursand": "Sizning kayfiyatingiz zo'r! Bugun nima yaxshi bo'ldi?",
        "g'amgin": "Tushunaman, ba'zida qiyin bo'ladi. Yordam bera olamanmi?",
        "g'azablangan": "Sakin bo'ling, muammoni birga hal qilamiz.",
        "qo'rqqan": "Xavotir olmang, men yordamchingizman.",
        "hayron": "Qiziqarli savol! Birga o'ylaymiz.",
        "bezovta": "Hamma narsa yaxshi bo'ladi. Nima bezovta qilyapti?",
        "tinch": "Yaxshi kayfiyat! Qanday yordam kerak?",
    }
    for key, val in responses.items():
        if key in emotion.lower():
            return val
    return ""

def process_emotion_command(text: str) -> str:
    text_lower = text.lower()

    if "hissiyot" in text_lower and "aniqla" in text_lower:
        result = detect_emotion(text)
        return f"Hissiyot: {result.get('emotion', 'noaniq')}"

    return detect_emotion(text).get("emotion", "Hissiyot aniqlanmadi.")
