import logging
import json
from scipy.spatial.distance import cosine
from app.common.models import Item, Recommend

# 주어진 카테고리에 따라 아이템들의 임베딩을 가져오는 함수
def get_embeddings_by_category(category_id):
    try:
        # 해당 카테고리에 속한 아이템들을 쿼리하여 가져옴
        items = Item.query.filter_by(category_id=category_id).all()
        embeddings = []
        for item in items:
            # 각 아이템의 추천 임베딩을 쿼리하여 가져옴
            recommend = Recommend.query.filter_by(recommend_id=item.recommend_id).first()
            if recommend and recommend.embedding:
                embedding = recommend.embedding
                if isinstance(embedding, str):
                    embedding = json.loads(embedding)  # JSON 문자열을 파싱하여 딕셔너리로 변환
                embeddings.append({
                    'id': item.item_id,
                    'embedding': embedding
                })
        return embeddings
    except Exception as e:
        logging.error(f"Error in get_embeddings_by_category: {e}")  # 오류 로깅
        return []

# 주어진 아이템 ID에 대한 임베딩 추천을 가져오는 함수
def get_embedding_recommendations(item_id):
    try:
        # 아이템을 쿼리하여 가져옴
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")

        # 해당 아이템의 추천 임베딩을 쿼리하여 가져옴
        recommend = Recommend.query.filter_by(recommend_id=item.recommend_id).first()
        if recommend is None or not recommend.embedding:
            raise ValueError(f"Recommend with ID {item.recommend_id} not found or no embedding found")

        current_embedding = recommend.embedding
        if isinstance(current_embedding, str):
            current_embedding = json.loads(current_embedding)  # JSON 문자열을 파싱하여 딕셔너리로 변환
        similarities = []
        
        # 동일 카테고리에 속한 다른 아이템들의 임베딩을 가져옴
        embeddings = get_embeddings_by_category(item.category_id)
        for embedding in embeddings:
            other_embedding = embedding['embedding']
            similarity = 1 - cosine(current_embedding, other_embedding)  # 코사인 유사도를 계산
            similarities.append({'item_id': embedding['id'], 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)  # 유사도에 따라 정렬
        return similarities[:12]  # 상위 12개의 유사한 아이템 반환
    except Exception as e:
        logging.error(f"Error in get_embedding_recommendations: {e}")  # 오류 로깅
        return []
