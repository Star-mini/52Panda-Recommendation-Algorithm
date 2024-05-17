from flask import Blueprint

bp = Blueprint('park', __name__)

from app.park import routes
