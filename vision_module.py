import os
import time

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from groq import Groq
    import base64
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_KEY = os.getenv("GROQ_API_KEY_1")
    groq_client = Groq(api_key=GROQ_KEY)
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False

def capture_image(save_path: str = None) -> str:
    if not CV2_AVAILABLE:
        return "Kamera moduli hozircha ishlamayapti."
    if save_path is None:
        save_path = os.path.expanduser("~/nuri/capture.jpg")
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Kamera topilmadi."
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite(save_path, frame)
            return save_path
        return "Rasm olishda xato."
    except Exception as e:
        return f"Xato: {e}"

def analyze_image(image_path: str) -> str:
    if not GROQ_AVAILABLE:
        return "AI tahlil hozircha ishlamayapti."
    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        response = groq_client.chat.completions.create(
            model="llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Bu rasmda nima ko'rinyapti? O'zbek tilida qisqa tavsif ber."
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Tahlil xato: {e}"

def capture_and_analyze() -> str:
    image_path = capture_image()
    if not image_path.endswith(".jpg"):
        return image_path
    return analyze_image(image_path)

def process_vision_command(text: str) -> str:
    text_lower = text.lower()

    if "rasm ol" in text_lower or "foto ol" in text_lower:
        return capture_image()

    elif "kamera" in text_lower and "ko'r" in text_lower:
        return capture_and_analyze()

    elif "nima ko'rinyapti" in text_lower or "atrofni ko'r" in text_lower:
        return capture_and_analyze()

    elif "tahlil qil" in text_lower and "rasm" in text_lower:
        parts = text.split("tahlil qil", 1)
        if len(parts) > 1:
            path = parts[1].strip()
            if os.path.exists(path):
                return analyze_image(path)
        return capture_and_analyze()

    return "Kamera buyrug'i tushunilmadi."
