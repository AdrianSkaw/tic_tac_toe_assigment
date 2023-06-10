from . import db
class Player(db.Model):
    name = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String, db.ForeignKey('symbol.symbol'), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        self.credits = 10
        self.symbol = None



