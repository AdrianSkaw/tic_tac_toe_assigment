from . import db
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    score = db.Column(db.Integer, nullable=False)



