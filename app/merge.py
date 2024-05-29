# app/merge.py

import logging
from scipy.spatial.distance import cosine
import json
import os
import requests
from app.item.image.algorithm import image_recommendations  # 수정된 경로로 import
from app.item.Embedding.algorithm import get_embeddings_by_category
from app.common.models import Item

def merge_and_send_recommendations(item_id):
    try:
        # 임베딩 추천 결과 가져오기
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")

        category_id = item.category_id
        embeddings = get_embeddings_by_category(category_id)

        if not item.embedding:
            raise ValueError('Embedding not found for the item')
        current_embedding = json.loads(item.embedding)

        similarities = []
        for embedding in embeddings:
            if embedding['embedding']:
                other_embedding = json.loads(embedding['embedding'])
                similarity = 1 - cosine(current_embedding, other_embedding)
                similarities.append({'item_id': embedding['id'], 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_embeddings = similarities[1:5]  # 상위 4개 선택

        # 아마존 알고리즘 호출
        image_recommendations_result = image_recommendations(item_id)

        # 병합 로직
        combined_recommendations = top_embeddings + image_recommendations_result
        combined_recommendations.sort(key=lambda x: x.get('similarity', x.get('score')), reverse=True)
        top_recommendations = combined_recommendations[:8]
        top_item_ids = [rec['item_id'] for rec in top_recommendations]

        logging.info(f"Top 8 combined recommendations: {top_item_ids}")

        # DTO로 변환 후 Spring Boot API 호출
        spring_boot_url = os.getenv('SPRING_BOOT_API_URL') + "/v1/no-auth/auction/Recommendation/makeDto"
        if not spring_boot_url:
            raise ValueError('Spring Boot API URL not set in environment variables')

        headers = {'Content-Type': 'application/json'}
        response = requests.post(spring_boot_url, json=top_item_ids, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Failed to call Spring Boot endpoint')

    except Exception as e:
        logging.error(f"Error in merge_and_send_recommendations: {e}")
        return None
