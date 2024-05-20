from app.common.extensions import db

class Item(db.Model):
    __tablename__ = 'Item'

    item_id = db.Column(db.Integer, primary_key=True)
    embedding = db.Column(db.Text, nullable=True)
