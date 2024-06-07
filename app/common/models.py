from app.common.extensions import db

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    is_auction_complete = db.Column(db.Boolean)
    category_id = db.Column(db.BigInteger)
    region_id = db.Column(db.BigInteger)
    seller_id = db.Column(db.BigInteger)
    trading_method_id = db.Column(db.BigInteger)

class Recommend(db.Model):
    __tablename__ = 'recommend'
    recommend_id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    embedding = db.Column(db.Text)
    th_embedding = db.Column(db.Text)
    category_embedding = db.Column(db.Text)
    detail_embedding = db.Column(db.Text)
    represent_embedding = db.Column(db.Text)
    item_id = db.Column(db.BigInteger, db.ForeignKey('item.item_id'))
    item = db.relationship('Item', backref=db.backref('recommendations', lazy=True))

class AuctionProgressItem(db.Model):
    __tablename__ = 'auction_progress_item'
    auction_progress_item_id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    bid_finish_time = db.Column(db.DateTime)
    buy_now_price = db.Column(db.Integer)
    item_title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    max_person_nick_name = db.Column(db.String(255))
    max_price = db.Column(db.Integer)
    start_price = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))
    item_id = db.Column(db.BigInteger, db.ForeignKey('item.item_id'))
    user_id = db.Column(db.BigInteger)