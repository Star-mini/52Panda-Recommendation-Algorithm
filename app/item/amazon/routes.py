from flask import Blueprint, request, jsonify
from .algorithm import process_item

item_bp = Blueprint('amazon', __name__)

@item_bp.route('/api/amazon', methods=['POST'])
def item():
    try:
        data = request.get_json()
        item_id = data.get('id')

        # 아이템 알고리즘 로직
        result = process_item(item_id)
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
