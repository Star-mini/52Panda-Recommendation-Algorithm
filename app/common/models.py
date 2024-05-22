from app.common.extensions import db

class Item(db.Model):
    __tablename__ = 'item'  # 데이터베이스 테이블 이름이 대문자 I로 시작하는지 확인하세요.

    item_id = db.Column(db.BigInteger, primary_key=True)  # 주키로 설정
    created_at = db.Column(db.DateTime)  # 생성 시각
    updated_at = db.Column(db.DateTime)  # 업데이트 시각
    is_auction_complete = db.Column(db.Boolean)  # 경매 완료 여부, BIT 타입은 SQLAlchemy에서 Boolean으로 매핑될 수 있습니다.
    category_id = db.Column(db.BigInteger)  # 카테고리 ID
    region_id = db.Column(db.BigInteger)  # 지역 ID
    seller_id = db.Column(db.BigInteger)  # 판매자 ID
    trading_method_id = db.Column(db.BigInteger)  # 거래 방식 ID
    embedding = db.Column(db.Text, nullable=True)  # 임베딩 데이터
