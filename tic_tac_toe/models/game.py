from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    wins = db.Column(db.String, db.ForeignKey('player.name'), nullable=True, default='No wins', )
    ties = db.Column(db.String, nullable=True, default='No ties')
    duration = db.Column(db.Float, nullable=True, default=0.0)
    

