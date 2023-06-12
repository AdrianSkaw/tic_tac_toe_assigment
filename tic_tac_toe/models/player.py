from . import db
class Player(db.Model):
    name = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String, db.ForeignKey('symbol.symbol'), nullable=False, unique=False)




