from flask import Blueprint

bp = Blueprint('son', __name__)

from app.son import routes
