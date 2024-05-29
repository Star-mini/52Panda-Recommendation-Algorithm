from flask import Blueprint

bp = Blueprint('son', __name__)

from app.user import routes
