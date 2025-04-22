
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ACCESS_KEY = os.getenv("ACCESS_KEY", '')
    SECRET_KEY = os.getenv("SECRET_KEY")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

