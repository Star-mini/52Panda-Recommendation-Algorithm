from flask import Blueprint, request, jsonify
import logging
from app.merge import merge_and_send_recommendations  # 경로 수정

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/Recommend', methods=['POST'])
def embedding():
    try:
        logging.info("Embedding route called")

        data = request.get_json()
        logging.info(f"Received data: {data}")

        item_id = data.get('id')
        user_id = data.get('user_id')  # 유저 ID를 요청 데이터에서 가져옴
        if not item_id:
            return jsonify({'status': 'fail', 'message': 'No item ID provided'}), 400

        result = merge_and_send_recommendations(item_id, user_id)

        if result:
            return jsonify({'status': 'success', 'data': result})
        else:
            return jsonify({'status': 'fail', 'message': 'Failed to merge recommendations'}), 500

    except Exception as e:
        logging.error(f"Error in embedding route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500
