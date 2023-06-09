from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref=db.backref('games', lazy=True))
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    ties = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    

