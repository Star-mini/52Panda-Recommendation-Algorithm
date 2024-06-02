from flask import Blueprint, jsonify
from app.common.extensions import db
from app.common.models import Recommend
import json

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
            for embed_str in [recommend.embedding, recommend.th_embedding, recommend.category_embedding, recommend.detail_embedding]:
                if embed_str:
                    embed_list = json.loads(embed_str)
                    embeddings.extend(embed_list)
            
            # 유효한 임베딩 값의 평균을 계산
            if embeddings:
                represent_embedding = sum(embeddings) / len(embeddings)
                # 계산된 평균 값을 represent_embedding 컬럼에 저장
                recommend.represent_embedding = json.dumps([represent_embedding])
                db.session.commit()
                return jsonify({"message": "Represent embedding updated successfully"}), 200
            else:
                return jsonify({"message": "No valid embeddings found"}), 400
        else:
            return jsonify({"message": "No recommendations found"}), 404
    except Exception as e:
        # 오류 발생 시 롤백
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
