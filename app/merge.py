import logging
from scipy.spatial.distance import cosine
import json
import os
import requests
from app.common.models import Item

def merge_and_send_recommendations(item_id):
    try:
        # 데이터베이스에서 해당 item_id의 아이템 객체를 가져옴
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")  # 아이템이 없으면 예외 발생

        category_id = item.category_id  # 아이템의 카테고리 ID 추출
        embeddings = get_embeddings_by_category(category_id)  # 해당 카테고리의 모든 임베딩 정보를 가져옴

        if not item.embedding:
            raise ValueError('Embedding not found for the item')  # 해당 아이템의 임베딩 정보가 없으면 예외 발생

        current_embedding = json.loads(item.embedding)  # JSON 문자열로 저장된 임베딩 정보를 파싱
        similarities = []

        # 카테고리 내 다른 아이템들의 임베딩과의 유사도 계산
        for embedding in embeddings:
            if embedding['embedding']:
                other_embedding = json.loads(embedding['embedding'])
                similarity = 1 - cosine(current_embedding, other_embedding)  # 코사인 유사도 계산
                similarities.append({'item_id': embedding['id'], 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)  # 유사도 기준으로 내림차순 정렬
        top_embeddings = similarities[:12]  # 상위 12개 아이템 선택

        # 로깅: 추천된 상위 12개 아이템의 ID를 로깅
        logging.info(f"Top 12 embedding recommendations: {[rec['item_id'] for rec in top_embeddings]}")

        return top_embeddings  # 추천 결과 반환
    except Exception as e:
        logging.error(f"Error in merge_and_send_recommendations: {e}")  # 에러 발생 시 로깅
        return None
