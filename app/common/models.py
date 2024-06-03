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
