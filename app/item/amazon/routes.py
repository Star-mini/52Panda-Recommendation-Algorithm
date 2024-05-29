# app/item/amazon/routes.py

from flask import Blueprint, request, jsonify
import logging
from .algorithm import process_item  # 상대 경로로 import
from .algorithm import amazon_recommendations

amazon_bp = Blueprint('amazon', __name__)

@amazon_bp.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    item_id = data.get('id')
    process_item(item_id)
    return jsonify({'status': 'success'})
