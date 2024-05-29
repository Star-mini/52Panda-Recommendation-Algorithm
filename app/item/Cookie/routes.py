from flask import Blueprint, request, jsonify
from .algorithm import process_cookie

cookie_bp = Blueprint('cookie', __name__)

@cookie_bp.route('/api/cookie', methods=['POST'])
def cookie():
    try:
        data = request.get_json()
        cookie_id = data.get('id')

        # 쿠키 알고리즘 로직
        result = process_cookie(cookie_id)
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
