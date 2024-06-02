from flask import Blueprint, request, jsonify
import logging
from app.merge import merge_and_send_recommendations  # 경로 수정

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/Recommend', methods=['POST'])
def embedding():
    try:
        logging.info("Embedding route called")  # 라우트 호출 로그

        data = request.get_json()  # 요청 데이터 JSON 파싱
        logging.info(f"Received data: {data}")  # 받은 데이터 로그

        item_id = data.get('id')  # 아이템 ID를 요청 데이터에서 가져옴
        user_id = data.get('user_id')  # 유저 ID를 요청 데이터에서 가져옴
        if not item_id:
            return jsonify({'status': 'fail', 'message': 'No item ID provided'}), 400  # 아이템 ID가 없을 때 응답

        # 추천 병합 및 전송 함수 호출
        result = merge_and_send_recommendations(item_id, user_id)

        if result:
            return jsonify({'status': 'success', 'data': result})  # 성공 시 응답
        else:
            return jsonify({'status': 'fail', 'message': 'Failed to merge recommendations'}), 500  # 실패 시 응답

    except Exception as e:
        logging.error(f"Error in embedding route: {e}")  # 오류 로깅
        return jsonify({'status': 'fail', 'message': str(e)}), 500  # 오류 응답
