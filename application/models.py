from .database import db

class Users(db.Model):
    user_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, unique=True, nullable=False)
    decks=db.relationship('Decks', backref='user')

class Decks(db.Model):
    __table_args__=(db.UniqueConstraint('deck_name','user_id'),)
    deck_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_name=db.Column(db.String, nullable=False)
    last_reviewed=db.Column(db.DateTime)
    Score=db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    flashcards=db.relationship('Cards', backref='deck')

class Cards(db.Model):
    __table_args__=(db.UniqueConstraint('front','back','deck_id'),)
    fc_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_id=db.Column(db.Integer, db.ForeignKey('decks.deck_id'), nullable=False)
    front=db.Column(db.String,nullable=False)
    back=db.Column(db.String, nullable=False)
    difficulty=db.Column(db.String)

class Globalcards(db.Model):
    gfc_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    gdeck_name=db.Column(db.String,nullable=False)
    gfront=db.Column(db.String,nullable=False)
    gback=db.Column(db.String,nullable=False)
    gdifficulty=db.Column(db.String)
