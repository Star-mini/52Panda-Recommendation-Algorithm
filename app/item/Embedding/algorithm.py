import logging
import json
from scipy.spatial.distance import cosine
from app.common.models import Item, Recommend

def get_embeddings_by_category(category_id):
    try:
        items = Item.query.filter_by(category_id=category_id).all()
        embeddings = []
        for item in items:
            recommend = Recommend.query.filter_by(recommend_id=item.recommend_id).first()
            if recommend and recommend.embedding:
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

def get_embedding_recommendations(item_id):
    try:
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")

        recommend = Recommend.query.filter_by(recommend_id=item.recommend_id).first()
        if recommend is None or not recommend.embedding:
            raise ValueError(f"Recommend with ID {item.recommend_id} not found or no embedding found")

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
        return similarities[:12]
    except Exception as e:
        logging.error(f"Error in get_embedding_recommendations: {e}")
        return []
