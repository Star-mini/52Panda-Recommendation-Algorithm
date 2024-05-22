from app.common.models import Item
from app.common.extensions import db
import json
import logging

def process_embedding(embedding_id):
    try:
        # 데이터베이스에서 임베딩 값 가져오기
        item = Item.query.filter_by(item_id=embedding_id).first()
        if item and item.embedding:
            embedding = json.loads(item.embedding)
            return {'id': embedding_id, 'embedding': embedding}
        else:
            raise ValueError(f"Item with id {embedding_id} not found or embedding is missing")
    except Exception as e:
        logging.error(f"Error in process_embedding: {e}")
        raise

def get_embeddings_by_category(category_id):
    try:
        # 해당 카테고리의 모든 아이템을 가져옴
        items = Item.query.filter_by(category_id=category_id).all()
        logging.info(f"Number of items retrieved: {len(items)}")  # 아이템 수 로깅
        embeddings = []
        for item in items:
            if item.embedding:
                embeddings.append({
                    'id': item.item_id,
                    'embedding': item.embedding  # JSON으로 파싱하지 않고 그대로 저장
                })
        # 임베딩 데이터를 가진 아이템의 수를 로깅
        logging.info(f"Number of items with embeddings: {len(embeddings)}")
        return embeddings
    except Exception as e:
        logging.error(f"Error in get_embeddings_by_category: {e}")
        return []
