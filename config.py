from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

CONTENT_TYPES = {
    'audio': [
        "audio/wav",
        "audio/mpeg",
        "audio/mp4",
    ],
    'video': [
        "video/mp4",
        "video/mov",
    ],
    'image': [
        "image/png",
        "image/jpeg",
    ],
    'document': [
        "application/pdf",
        "application/x-excel",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
}
