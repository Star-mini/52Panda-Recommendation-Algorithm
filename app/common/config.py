import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 로깅 설정
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
