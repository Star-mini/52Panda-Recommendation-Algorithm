from flask import Blueprint, jsonify
from app.common.extensions import db
from app.common.models import Recommend
import json
import numpy as np  # numpy를 사용하여 평균 계산

# Blueprint 객체 생성
make_represent_bp = Blueprint('make_represent', __name__)

# GET 요청에 대한 라우트 정의
@make_represent_bp.route('/MakeRepresentEmbedding', methods=['GET'])
def make_represent_embedding():
    try:
        # Recommend 테이블에서 가장 최근 레코드 조회
        recommend = Recommend.query.order_by(Recommend.recommend_id.desc()).first()
        if recommend:
            # 각 레코드의 임베딩 값을 리스트에 저장 (null 값 제외)
            embeddings = []
            weights = [5, 2, 2, 3]  # 카테고리, 상세설명, 제목, 썸네일의 가중치
            weight_sum = sum(weights)  # 가중치 합산
            
            for idx, embed_str in enumerate([recommend.embedding, recommend.th_embedding, recommend.category_embedding, recommend.detail_embedding]):
                if embed_str:
                    embed_list = json.loads(embed_str)
                    weighted_embed = np.array(embed_list) * weights[idx]  # 가중치 적용
                    embeddings.append(weighted_embed)
            
            if embeddings:
                # 배열을 전치하여 동일 인덱스 위치에 있는 값을 그룹화
                transposed_embeddings = np.array(embeddings).T
                
                # 각 그룹에 대해 평균 계산
                represent_embedding = np.sum(transposed_embeddings, axis=1) / weight_sum
                represent_embedding = represent_embedding.tolist()
                
                # 계산된 평균 값을 represent_embedding 컬럼에 저장
                recommend.represent_embedding = json.dumps(represent_embedding)
                db.session.commit()
                return jsonify({"message": "Represent embedding updated successfully"}), 200
            else:
                return jsonify({"message": "No valid embeddings found"}), 404
        else:
            return jsonify({"message": "No recommendations found"}), 404
    except Exception as e:
        # 오류 발생 시 롤백
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
