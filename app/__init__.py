from flask import Flask
from app.common.config import Config
from app.common.extensions import db
from app.item.Embedding.routes import embedding_bp  # 기존 경로
from app.item.amazon.routes import amazon_bp  # 변경된 경로
from app.item.Cookie.routes import cookie_bp  # 기존 경로
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # 로깅 설정
    logging.basicConfig(level=app.config.get("LOGGING_LEVEL", "DEBUG"))
    
    # Blueprint 등록
    app.register_blueprint(embedding_bp, url_prefix='/api')
    app.register_blueprint(amazon_bp, url_prefix='/api')  # 경로 변경
    app.register_blueprint(cookie_bp, url_prefix='/api')
    
    return app
