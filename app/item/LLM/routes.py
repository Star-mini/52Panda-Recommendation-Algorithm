from flask import Blueprint

llm_bp = Blueprint('llm_bp', __name__)

@llm_bp.route('/llm')
def llm_home():
    return "Welcome to the LLM module!"
