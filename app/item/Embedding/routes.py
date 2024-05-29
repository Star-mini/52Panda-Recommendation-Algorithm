import os
from flask import Blueprint, request, jsonify
from app.item.Embedding.algorithm import process_embedding, get_embeddings_by_category  # 경로 수정
import logging
from app.common.models import Item
import json
from scipy.spatial.distance import cosine
import requests
from dotenv import load_dotenv

load_dotenv()

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/Recommend', methods=['POST'])  # 경로 수정
def embedding():
    try:
        logging.info("Embedding route called")  # 디버그 메시지 추가

        # JSON 데이터를 받아옴
        data = request.get_json()

        # 받은 데이터를 출력
        logging.info(f"Received data: {data}")

        # 데이터에서 id 값을 추출
        item_id = data.get('id')

        if not item_id:
            return jsonify({'status': 'fail', 'message': 'No item ID provided'}), 400

        # 해당 ID로 category_embeddings 로직 호출
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            return jsonify({'status': 'fail', 'message': f'Item with ID {item_id} not found'}), 404

        category_id = item.category_id
        embeddings = get_embeddings_by_category(category_id)

        # 현재 아이템의 임베딩을 로드합니다
        if not item.embedding:
            return jsonify({'status': 'fail', 'message': 'Embedding not found for the item'}), 404
        current_embedding = json.loads(item.embedding)

        # 코사인 유사도 계산
        similarities = []
        for embedding in embeddings:
            if embedding['embedding']:
                other_embedding = json.loads(embedding['embedding'])
                similarity = 1 - cosine(current_embedding, other_embedding)
                similarities.append({
                    'item_id': embedding['id'],
                    'similarity': similarity
                })

        # 유사도를 기준으로 내림차순 정렬
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        # 상위 8개만 선택 (자기 자신 제외)
        top_similarities = similarities[1:9]
        top_item_ids = [similarity['item_id'] for similarity in top_similarities]

        logging.info(f"Top 8 similar items: {top_item_ids}")

        # 환경변수에서 스프링 부트 API URL을 읽어옴
        spring_boot_url = os.getenv('SPRING_BOOT_API_URL') + "/v1/no-auth/auction/Recommendation/Embedding/makeDto"
        if not spring_boot_url:
            return jsonify({'status': 'fail', 'message': 'Spring Boot API URL not set in environment variables'}), 500

        headers = {'Content-Type': 'application/json'}
        response = requests.post(spring_boot_url, json=top_item_ids, headers=headers)

        if response.status_code == 200:
            return jsonify({'status': 'success', 'data': response.json()})
        else:
            return jsonify({'status': 'fail', 'message': 'Failed to call Spring Boot endpoint'}), response.status_code

    except Exception as e:
        logging.error(f"Error in embedding route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500