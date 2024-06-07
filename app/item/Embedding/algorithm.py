import logging
import json
from scipy.spatial.distance import cosine
from app.common.models import Item, Recommend, AuctionProgressItem

# 주어진 카테고리에 따라 아이템들의 임베딩을 가져오는 함수
def get_embeddings_by_category(category_id):
    try:
        items = Item.query.filter_by(category_id=category_id).all()  # 주어진 카테고리에 속하는 모든 아이템 가져오기
        embeddings = []
        for item in items:
            for recommend in item.recommendations:
                if recommend.represent_embedding:
                    represent_embedding = recommend.represent_embedding
                    if isinstance(represent_embedding, str):
                        represent_embedding = json.loads(represent_embedding)  # 문자열 형태의 임베딩을 JSON으로 파싱
                    embeddings.append({
                        'id': item.item_id,
                        'embedding': represent_embedding
                    })
        return embeddings
    except Exception as e:
        logging.error(f"Error in get_embeddings_by_category: {e}")  # 에러 로그 남기기
        return []

# 주어진 아이템 ID에 대한 임베딩 추천을 가져오는 함수
def get_embedding_recommendations(item_id):
    try:
        item = Item.query.filter_by(item_id=item_id).first()  # 주어진 아이템 ID에 해당하는 아이템 가져오기
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")  # 아이템이 없을 경우 예외 발생

        # 아이템이 경매 중인지 확인
        auction_item = AuctionProgressItem.query.filter_by(item_id=item_id).first()
        if auction_item is None:
            raise ValueError(f"Auction item with ID {item_id} not found")  # 경매 중인 아이템이 없을 경우 예외 발생

        recommendations = item.recommendations
        if not recommendations:
            raise ValueError(f"No recommendations found for item ID {item_id}")  # 추천 임베딩이 없을 경우 예외 발생

        current_embeddings = []
        for recommend in recommendations:
            if recommend.represent_embedding:
                current_embedding = recommend.represent_embedding
                if isinstance(current_embedding, str):
                    current_embedding = json.loads(current_embedding)  # 문자열 형태의 임베딩을 JSON으로 파싱
                current_embeddings.append(current_embedding)

        similarities = []
        
        # 동일 카테고리의 모든 임베딩 가져오기
        embeddings = get_embeddings_by_category(item.category_id)
        for embedding in embeddings:
            other_item_id = embedding['id']
            other_auction_item = AuctionProgressItem.query.filter_by(item_id=other_item_id).first()
            
            # max_price 조건 확인
            if other_auction_item and other_auction_item.max_price <= 2 * auction_item.max_price:
                other_embeddings = embedding['embedding']
                for current_embedding in current_embeddings:
                    similarity = 1 - cosine(current_embedding, other_embeddings)  # 코사인 유사도로 임베딩 간 유사도 계산
                    similarities.append({'item_id': other_item_id, 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)  # 유사도 순으로 정렬
        return similarities[1:12]  # 가장 유사한 11개 아이템 반환 (자기 자신 제외)
    except Exception as e:
        logging.error(f"Error in get_embedding_recommendations: {e}")  # 에러 로그 남기기
        return []

# 로깅 설정
logging.basicConfig(level=logging.INFO)
