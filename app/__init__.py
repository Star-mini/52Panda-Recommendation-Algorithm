from flask import Flask
from app.common.config import Config
from app.common.extensions import db
from app.item.Embedding.routes import embedding_bp  # 경로 수정
from app.item.Item.routes import item_bp  # 경로 수정
from app.item.Cookie.routes import cookie_bp  # 경로 수정
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
    app.register_blueprint(item_bp, url_prefix='/api')
    app.register_blueprint(cookie_bp, url_prefix='/api')
    
    return app
