from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    wins = db.Column(db.String, db.ForeignKey('player.name'), nullable=False, default='No wins', )
    ties = db.Column(db.String, nullable=False, default='No ties')
    duration = db.Column(db.Integer, nullable=False)
    

