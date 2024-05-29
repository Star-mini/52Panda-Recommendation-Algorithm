# app/item/image/routes.py

from flask import Blueprint, request, jsonify
import logging
from .algorithm import process_item  # 상대 경로로 import
from .algorithm import image_recommendations

image_bp = Blueprint('image', __name__)

@image_bp.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    item_id = data.get('id')
    process_item(item_id)
    return jsonify({'status': 'success'})
