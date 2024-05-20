import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://panda:0000@localhost:3306/panda'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 로깅 설정
    LOGGING_LEVEL = 'DEBUG'
