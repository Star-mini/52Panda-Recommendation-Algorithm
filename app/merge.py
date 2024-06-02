import logging
import json
import os
import requests
from app.item.Embedding.algorithm import get_embedding_recommendations  # 임베딩 추천 함수 임포트
from app.common.models import Item

# 쿠키 기반 추천 함수 (예시)
def get_cookie_recommendations(item_id):
    recommendations = []  # 쿠키 기반 추천 결과를 여기에 추가
    return recommendations

# 유저 기반 추천 함수 (예시)
def get_user_recommendations(user_id):
    recommendations = []  # 유저 기반 추천 결과를 여기에 추가
    return recommendations

# 모든 추천 결과를 병합하는 함수
def merge_and_send_recommendations(item_id, user_id=None):
    try:
        embedding_recommendations = get_embedding_recommendations(item_id)
        cookie_recommendations = get_cookie_recommendations(item_id)
        user_recommendations = get_user_recommendations(user_id) if user_id else []

        combined_recommendations = embedding_recommendations + cookie_recommendations + user_recommendations
        combined_recommendations.sort(key=lambda x: x.get('similarity', x.get('score', 0)), reverse=True)
        top_recommendations = combined_recommendations[:12]

        logging.info(f"Top 12 combined recommendations: {[rec['item_id'] for rec in top_recommendations]}")
        top_item_ids = [rec['item_id'] for rec in top_recommendations]

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
