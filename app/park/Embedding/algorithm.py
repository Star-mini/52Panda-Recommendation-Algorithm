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
