import numpy as np
from gensim.models import Word2Vec
import faiss

def like_algorithm():
    # like 알고리즘 구현
# 해당 아이템을 찜한 사용자 조회
    like_items = LikeItem.query.filter_by(itemId=item_id).all()
    user_ids = [li.userId for li in like_items]

# 사용자가 찜한 다른 아이템 조회 및 가중치 부여
    item_weights = {}
    for user_id in user_ids:
        user_like_items = LikeItem.query.filter_by(userId=user_id).all()
        for uli in user_like_items:
            if uli.itemId != item_id:
                if uli.itemId in item_weights:
                    item_weights[uli.itemId] += 1
                else:
                    item_weights[uli.itemId] = 1

 # 가중치를 적용한 추천 아이템 리스트 생성
    weighted_items = []
    for item, weight in item_weights.items():
        weighted_items.extend([item] * weight)

# FAISS를 사용하여 유사 아이템 추가
    similar_items = find_similar_items(item_id, top_n=10)
    for sim_item in similar_items:
        if sim_item in item_weights:
            weighted_items.extend([sim_item] * (item_weights[sim_item] + 1))  # 유사 아이템에 추가 가중치 부여
        else:
            weighted_items.append(sim_item)

# 사전 학습된 Word2Vec 모델 로드 (모델 파일 경로는 실제 경로로 수정)
w2v_model = Word2Vec.load("path/to/your/word2vec/model")

# Faiss 인덱스 생성
d = 128  # 벡터 차원 수 (Word2Vec 모델의 벡터 크기와 일치해야 함)
index = faiss.IndexFlatL2(d)
embeddings = {}  # 임베딩 데이터를 저장할 딕셔너리

def find_similar_items(item_id, top_n=10):
    if item_id in embeddings:
        item_embedding = embeddings[item_id]
        distances, indices = index.search(np.array([item_embedding]), top_n)
        return [list(embeddings.keys())[idx] for idx in indices[0]]
    
    return {"message": "This is Son's recommendation"}
