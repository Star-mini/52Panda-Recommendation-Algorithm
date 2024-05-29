from flask import Blueprint, request, jsonify
from .algorithm import process_item

amazon_bp = Blueprint('amazon', __name__)  # 'amazon'으로 변경

@amazon_bp.route('/api/amazon', methods=['POST'])  # 라우트 이름 변경
def amazon():  # 함수 이름도 item에서 amazon으로 변경
    try:
        data = request.get_json()
        item_id = data.get('id')

        # 아이템 알고리즘 로직
        result = process_item(item_id)
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
