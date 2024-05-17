from flask import Flask
from app.common.config import Config
from app.common.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # 공통 블루프린트 등록
        from app.park import bp as park_bp
        from app.son import bp as son_bp
        app.register_blueprint(park_bp)
        app.register_blueprint(son_bp)

    return app
