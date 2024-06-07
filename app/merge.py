import logging
import json
import os
import requests
from app.item.Embedding.algorithm import get_embedding_recommendations
from app.common.models import Item

# 특정 아이템의 쿠키 추천을 가져오는 함수
def get_cookie_recommendations(item_id):
    recommendations = []
    return recommendations

# 특정 사용자의 추천을 가져오는 함수
def get_user_recommendations(user_id):
    recommendations = []
    return recommendations

# 아이템과 사용자 정보를 기반으로 추천을 병합하고 전송하는 함수
def merge_and_send_recommendations(item_id, user_id=None):
    try:
        # 임베딩 추천을 가져옴
        embedding_recommendations = get_embedding_recommendations(item_id)
        # 쿠키 추천을 가져옴
        cookie_recommendations = get_cookie_recommendations(item_id)
        # 사용자 추천을 가져옴 (user_id가 주어진 경우)
        user_recommendations = get_user_recommendations(user_id) if user_id else []

        # 모든 추천을 병합
        combined_recommendations = embedding_recommendations + cookie_recommendations + user_recommendations
        # 추천 리스트를 유사도 또는 점수를 기준으로 내림차순 정렬
        combined_recommendations.sort(key=lambda x: x.get('similarity', x.get('score', 0)), reverse=True)
        # 상위 12개의 추천 아이템을 선택
        top_recommendations = combined_recommendations[:12]

        logging.info(f"Top 12 combined recommendations: {[rec['item_id'] for rec in top_recommendations]}")
        top_item_ids = [rec['item_id'] for rec in top_recommendations]

        # Spring Boot API URL을 환경 변수에서 가져옴
        spring_boot_url = os.getenv('SPRING_BOOT_API_URL') + "/v1/no-auth/auction/Recommendation/makeDto"
        if not spring_boot_url:
            raise ValueError('Spring Boot API URL not set in environment variables')

        headers = {'Content-Type': 'application/json'}
        # Spring Boot API에 추천 아이템을 전송
        response = requests.post(spring_boot_url, json=top_item_ids, headers=headers)

        # 응답이 성공적이면 JSON 형태로 반환
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Failed to call Spring Boot endpoint')

    except Exception as e:
        logging.error(f"Error in merge_and_send_recommendations: {e}")
        return None
