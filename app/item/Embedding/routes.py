# app/item/Embedding/routes.py

from app.merge import merge_and_send_recommendations
from flask import Blueprint, request, jsonify
import logging

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/Recommend', methods=['POST'])
def embedding():
    try:
        logging.info("Embedding route called")

        data = request.get_json()
        logging.info(f"Received data: {data}")

        item_id = data.get('id')
        if not item_id:
            return jsonify({'status': 'fail', 'message': 'No item ID provided'}), 400

        result = merge_and_send_recommendations(item_id)

        if result:
            return jsonify({'status': 'success', 'data': result})
        else:
            return jsonify({'status': 'fail', 'message': 'Failed to merge recommendations'}), 500

    except Exception as e:
        logging.error(f"Error in embedding route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500
