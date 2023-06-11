from . import db

class Symbol(db.Model):
    symbol = db.Column(db.String, primary_key=True, nullable=False, unique=True)