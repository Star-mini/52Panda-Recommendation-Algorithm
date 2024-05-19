from flask import Blueprint, request, jsonify
from .algorithm import process_embedding

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/embedding', methods=['POST'])
def embedding():
    try:
        data = request.get_json()
        embedding_id = data.get('id')

        # 임베딩 알고리즘 로직
        result = process_embedding(embedding_id)
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
