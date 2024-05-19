from flask import Flask
from app.common.config import Config
from app.park.Embedding.routes import embedding_bp
from app.park.Item.routes import item_bp
from app.park.Cookie.routes import cookie_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Blueprint 등록
    app.register_blueprint(embedding_bp, url_prefix='/api')
    app.register_blueprint(item_bp, url_prefix='/api')
    app.register_blueprint(cookie_bp, url_prefix='/api')

    return app
