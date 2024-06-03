from flask import Blueprint

bp = Blueprint('like', __name__)

from app.user import routes
