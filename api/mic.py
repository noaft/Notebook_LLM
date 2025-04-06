import speech_recognition as sr
from fastapi import APIRouter
from api.upload import model
from api.user import LLM_model
from pydantic import BaseModel

router = APIRouter()

def record_and_transcribe_google(duration=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Đang thu âm...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source, duration=duration)
        print("🛑 Dừng thu âm.")

    # Chuyển đổi giọng nói thành văn bản
    try:
        text = recognizer.recognize_google(audio_data, language="vi-VN")
        return text
    except sr.UnknownValueError:
        return "🚫 Không thể nhận diện giọng nói"
    except sr.RequestError:
        return "⚠️ Lỗi kết nối đến API"

class User(BaseModel):
    file_name: list[str] # file name choose


@router.post("/mic")
def get_text(user: User):
    message = record_and_transcribe_google(20)
    context = model.search(message, user.file_name)
    respone = LLM_model.get_respone(context, message) # get respone
    return {"context": context, "respone": respone}