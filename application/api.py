from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse
from flask_security import login_required, auth_required
from flask_login import current_user
from application.database import db
from application.models import Deck, Card
from application.validation import NotFoundError, BusinessValidationError


deck_output = {
    "deck_id": fields.Integer,
    "title": fields.String,
    "last_review_date": fields.String,
    "score": fields.Integer
}

card_output = {
    "card_id": fields.Integer,
    "deck_id": fields.Integer,
    "word": fields.String,
    "translation": fields.String
}

create_deck_parser = reqparse.RequestParser()
create_deck_parser.add_argument('title')

update_deck_parser = reqparse.RequestParser()
update_deck_parser.add_argument('title')

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('deck_id')
create_card_parser.add_argument('word')
create_card_parser.add_argument('translation')


class DecksAPI(Resource):

    # @auth_required('token')
    # @login_required
    def get(self):
        print("GET decks")
        decks = Deck.query.all()
        if decks:
            decks_list = [{"deck_id": deck.deck_id, "title": deck.title, "last_review_date": str(deck.last_review_date), "score": deck.score} for deck in decks]
            return {"decks": decks_list}
        else:
            raise NotFoundError(status_code=404)


class DeckAPI(Resource):

    @marshal_with(deck_output)
    def get(self, deck_id):
        print("GET a deck")
        deck = Deck.query.filter_by(deck_id=deck_id).first()
        if deck:
            return deck
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(deck_output)
    def put(self, deck_id):
        print("PUT a deck")
        args = update_deck_parser.parse_args()
        title = args.get("title", None)
        if title is None:
            raise BusinessValidationError(status_code=400, error_code='BE1001', error_message='title is required')

        deck = Deck.query.filter_by(title=title).first()
        if deck:
            raise BusinessValidationError(status_code=400, error_code='BE1003', error_message='Deck with same name exists')

        deck = Deck.query.filter_by(deck_id=deck_id).first()
        if deck is None:
            raise NotFoundError(status_code=404)
        
        deck.title = title
        db.session.commit()
        return deck

    def delete(self, deck_id):
        print("DELETE a deck")
        deck = Deck.query.filter_by(deck_id=deck_id).first()
        if deck is None:
            raise NotFoundError(status_code=404)
        Card.query.filter_by(deck_id=deck_id).delete()
        Deck.query.filter_by(deck_id=deck_id).delete()
        db.session.commit()
        return "", 200

    @marshal_with(deck_output)
    def post(self):
        print("POST a deck")
        args = create_deck_parser.parse_args()
        title = args.get("title", None)
        if title is None:
            raise BusinessValidationError(status_code=400, error_code='BE1001', error_message='title is required')

        deck = Deck.query.filter_by(title=title).first()
        if deck:
            raise BusinessValidationError(status_code=400, error_code='BE1002', error_message='Duplicate deck')

        deck = Deck(title=title)
        db.session.add(deck)
        db.session.commit()
        return deck, 201


class CardAPI(Resource):

    @marshal_with(card_output)
    def post(self):
        print("POST a card")
        args = create_card_parser.parse_args()
        deck_id = args.get("deck_id", None)
        word = args.get("word", None)
        translation = args.get("translation", None)
        if word is None:
            raise BusinessValidationError(status_code=400, error_code='BE1004', error_message='word is required')
        if translation is None:
            raise BusinessValidationError(status_code=400, error_code='BE1005', error_message='translation is required')

        card = Card.query.filter_by(deck_id=deck_id).filter_by(word=word).first()
        if card:
            raise BusinessValidationError(status_code=400, error_code='BE1006', error_message='Duplicate card in same deck')

        card = Card(deck_id=deck_id, word=word, translation=translation)
        db.session.add(card)
        db.session.commit()
        return card, 201

    @marshal_with(card_output)
    def get(self, deck_id, word):
        print("GET a card")
        word = word.lower()
        card = Card.query.filter(Card.deck_id==deck_id).filter(Card.word==word).first()
        if card:
            return card
        else:
            raise NotFoundError(status_code=404)


class UserAPI(Resource):
    
    # @marshal_with(user_output)
    def get(self):
        if current_user.is_authenticated:
            return {"username": current_user.username}
        return ""

    def post(self):
        pass
