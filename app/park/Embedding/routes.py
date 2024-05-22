from flask import Blueprint, request, jsonify
from .algorithm import process_embedding, get_embeddings_by_category
import logging
from app.common.models import Item  # 올바른 경로로 Item을 임포트


embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/embedding', methods=['POST'])
def embedding():
    try:
        logging.info("Embedding route called")  # 디버그 메시지 추가
        # JSON 데이터를 받아옴
        data = request.get_json()
        
        # 받은 데이터를 출력
        logging.info(f"Received data: {data}")
        
        # 데이터에서 id 값을 추출
        embedding_id = data.get('id')

        # 임베딩 알고리즘 로직
        result = process_embedding(embedding_id)
        
        # 결과를 출력
        logging.info(f"Embedding result: {result}")
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        logging.error(f"Error in embedding route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@embedding_bp.route('/category_embeddings', methods=['POST'])
def category_embeddings():
    try:
        logging.info("Category embeddings route called")
        data = request.get_json()
        logging.info(f"Received data: {data}")

        item_id = data.get('item_id')
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            return jsonify({'status': 'fail', 'message': 'Item not found'}), 404

        category_id = item.category_id
        embeddings = get_embeddings_by_category(category_id)

        logging.info(f"Category embeddings result: {embeddings}")
        return jsonify({'status': 'success', 'data': embeddings})
    except Exception as e:
        logging.error(f"Error in category_embeddings route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500
