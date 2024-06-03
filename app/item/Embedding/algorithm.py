import logging
import json
from scipy.spatial.distance import cosine
from app.common.models import Item, Recommend

# 주어진 카테고리에 따라 아이템들의 임베딩을 가져오는 함수
def get_embeddings_by_category(category_id):
    try:
        items = Item.query.filter_by(category_id=category_id).all()
        embeddings = []
        for item in items:
            for recommend in item.recommendations:
                if recommend.embedding:
                    embedding = recommend.embedding
                    if isinstance(embedding, str):
                        embedding = json.loads(embedding)
                    embeddings.append({
                        'id': item.item_id,
                        'embedding': embedding
                    })
        return embeddings
    except Exception as e:
        logging.error(f"Error in get_embeddings_by_category: {e}")
        return []

# 주어진 아이템 ID에 대한 임베딩 추천을 가져오는 함수
def get_embedding_recommendations(item_id):
    try:
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")

        recommend = item.recommendations[0]  # 첫 번째 추천 임베딩 사용
        if recommend is None or not recommend.embedding:
            raise ValueError(f"No embedding found for item ID {item_id}")

        current_embedding = recommend.embedding
        if isinstance(current_embedding, str):
            current_embedding = json.loads(current_embedding)
        similarities = []
        
        embeddings = get_embeddings_by_category(item.category_id)
        for embedding in embeddings:
            other_embedding = embedding['embedding']
            similarity = 1 - cosine(current_embedding, other_embedding)
            similarities.append({'item_id': embedding['id'], 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[1:12]
    except Exception as e:
        logging.error(f"Error in get_embedding_recommendations: {e}")
        return []
