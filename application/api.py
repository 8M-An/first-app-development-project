from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import ValidationError, NotFoundError
from application.models import Users,Decks,Cards
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort

#request parsers
  #deck parser
deck_parser1=reqparse.RequestParser()
deck_parser1.add_argument('deck_name')

  #card parser
card_parser=reqparse.RequestParser()
card_parser.add_argument('front')
card_parser.add_argument('back')
card_parser.add_argument('deck_id')
card_parser.add_argument('difficulty')

   #user parser



#output fields format
deck_fields={'deck_id':fields.Integer, 'deck_name':fields.String, 'last_reviewed': fields.String, 'Score':fields.Integer, 'user_id':fields.Integer}
card_fields={'fc_id': fields.Integer, 'deck_id':fields.Integer, 'front':fields.String, 'back':fields.String, 'difficulty':fields.String}



class Deck_api(Resource):
    #get method for decks
    @marshal_with(deck_fields)
    def get(self,deck_id,uname,psw):
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        if not user:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        flashcards=Cards.query.filter(Cards.deck_id==deck_id).all()
        if deck:
            if not deck.user_id==user.user_id:
                raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')
            return deck
        else:
            raise NotFoundError(status_code=404)

    #post method:creates new resource
    def post(self,uname,psw):
        args=deck_parser1.parse_args()
        deck_name=args.get('deck_name',None)
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        if not user:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')
        if deck_name is None:
            raise ValidationError(status_code=400,error_code='DECK002',error_message='deck name is required')

        deck=Decks(deck_name=args['deck_name'],user_id=user.user_id)
        db.session.add(deck)
        db.session.commit()
        return 'Successfully created',201

    #put method:updating existing decks
    def put(self,deck_id,uname,psw):
        args=deck_parser1.parse_args()
        deck_name=args.get('deck_name',None)
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        if not user:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        if deck is None:
            raise NotFoundError(status_code=404)
        if deck_name is None:
            raise ValidationError(status_code=400,error_code='DECK002',error_message='deck name is required')
        if not (deck.user_id==user.user_id):
            raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')

        deck.deck_name=deck_name
        db.session.commit()
        return 'Successfully Updated',200

    #delete method:delete deck
    def delete(self,deck_id,uname,psw):
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        if not user:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        if deck is None:
            raise NotFoundError(status_code=404)
        if not (deck.user_id==user.user_id):
            raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')

        c=Cards.query.filter(Cards.deck_id==deck_id).all()
        if c!=[]:
            for i in c:
                db.session.delete(i)
        db.session.delete(deck)
        db.session.commit()
        return 'Successfully Deleted',200


class Card_api(Resource):

    #get card
    @marshal_with(card_fields)
    def get(self,fc_id,uname,psw):
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        card=Cards.query.filter(Cards.fc_id==fc_id).first()
        if user:
            if card:
                deck=Decks.query.filter(Decks.deck_id==card.deck_id).first()                
                if not (deck.user_id==user.user_id):
                    raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')
                return card
            else:
                raise NotFoundError(status_code=404)
        else:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')



    #creating new card
    def post(self,uname,psw):
        args=card_parser.parse_args()
        front=args.get('front',None)
        back=args.get('back',None)
        deck_id=args.get('deck_id',None)
        difficulty=args.get('difficulty',None)
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        if not user:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')
        if deck_id is None:
            raise ValidationError(status_code=400,error_code='CARD001',error_message='Deck id is required')
        if front is None:
            raise ValidationError(status_code=400,error_code='CARD002',error_message='Front is required')
        if back is None:
            raise ValidationError(status_code=400,error_code='CARD003',error_message='Back is required')

        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        if not (deck.user_id==user.user_id):
            raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')
        flashcard=Cards(front=front,deck_id=deck_id,back=back,difficulty=difficulty)
        db.session.add(flashcard)
        db.session.commit()
        return 'Successfully created',201



    #update card
    def put(self,fc_id,uname,psw):
        args=card_parser.parse_args()
        front=args.get('front',None)
        back=args.get('back',None)
        difficulty=args.get('difficulty',None)
        deck_id=args.get('deck_id',None)
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        flashcard=Cards.query.filter(Cards.fc_id==fc_id).first()
        if not deck_id:
            raise NotFoundError(status_code=404)

        if user:
            deck=Decks.query.filter(Decks.deck_id==deck_id).first()
            if not (deck.user_id==user.user_id):
                raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')

            if flashcard is None:
                raise NotFoundError(status_code=404)
            if front is not None:
                flashcard.front=front
            if back is not None:
                flashcard.back=back
            flashcard.difficulty=difficulty
            db.session.commit()
            return 'Successfully updated',200
        else:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')



    #delete card
    def delete(self,fc_id,uname,psw):
        user=Users.query.filter(Users.username==uname,Users.password==psw).first()
        flashcard=Cards.query.filter(Cards.fc_id==fc_id).first()
        if user:
            if flashcard is None:
                raise NotFoundError(status_code=404)
            deck=Decks.query.filter(Decks.deck_id==flashcard.deck_id).first()
            if not (deck.user_id==user.user_id):
                raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')

            db.session.delete(flashcard)
            db.session.commit()
            return 'Successfully deleted',200
        else:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')



class cards_of_deck_api(Resource):
    #get all cards of a deck
    @marshal_with(card_fields)
    def get(self,deck_id,username,password):
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        user=Users.query.filter(Users.username==username,Users.password==password).first()
        if user:
            if deck:
                deck=Decks.query.filter(Decks.deck_id==deck_id).first()
                if not (deck.user_id==user.user_id):
                    raise ValidationError(status_code=400, error_code='USER002', error_message='Deck does not belong to user')
                cards=Cards.query.filter(Cards.deck_id==deck_id).all()
                if cards!=[]:
                    return cards
                else:
                    raise ValidationError(status_code=400,error_code='DECK003',error_message='Deck is empty')
            else:
                raise ValidationError(status_code=400, error_code='DECK004', error_message='Deck does not exist')
        else:
            raise ValidationError(status_code=400, error_code='USER001', error_message='User does not exist')

class decks_of_user_api(Resource):
    #get all cards of a deck
    @marshal_with(deck_fields)
    def get(self,username,password):
        user=Users.query.filter(Users.username==username,Users.password==password).first()
        if user:
            decks=Decks.query.filter(Decks.user_id==user.user_id).all()
            if decks!=[]:
                return decks
            else:
                raise ValidationError(status_code=400,error_code='USER003',error_message='User has no decks')
        else:
            raise NotFoundError(status_code=404)
