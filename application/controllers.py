
from flask import render_template
from random import randrange
from sqlalchemy.sql import func
from flask import request, current_app as app
from flask_security import login_required, roles_required

from application.database import db
from application.models import Deck, Card
from application import tasks


@app.route("/", methods=["GET", "POST"])
def decks():
    # decks = Deck.query.all()
    # return render_template("index.html", decks=decks)
    return render_template("index.html")

# @app.route("/deck/create", methods=["GET", "POST"])
@app.route("/deck/create", methods=["GET"])
@login_required
def add_deck():
    return render_template("add_deck.html")
    # if request.method == "GET":
    #     return render_template("add_deck.html")
    # elif request.method== "POST":
    #     title = request.form['title']
    #     deck = Deck(title=title)
    #     db.session.add(deck)
    #     db.session.commit()
    #     decks = Deck.query.all()
    #     return render_template("index.html", decks=decks)
    # else:
    #     print("Error check")

@app.route("/deck/<deck_id>", methods=["GET"])
# @app.route("/deck/<deck_id>", methods=["GET", "POST"])
def get_deck(deck_id):
    return render_template("deck.html")
    # deck = Deck.query.filter_by(deck_id=deck_id).first()
    # return render_template("deck.html", deck=deck)

# @app.route("/deck/<deck_id>/update", methods=["GET", "POST"])
@app.route("/deck/<deck_id>/update", methods=["GET"])
@login_required
def update_deck(deck_id):
    return render_template("edit_deck.html", deck_id=deck_id)
    # if request.method == "GET":
    #     return render_template("edit_deck.html", deck_id=deck_id)
    # elif request.method== "POST":
    #     deck = Deck.query.filter_by(deck_id=deck_id).first()
    #     deck.title = request.form['title']
    #     # Deck.query.filter_by(deck_id=deck_id).title = request.form['title']
    #     db.session.commit()
    #     decks = Deck.query.all()
    #     return render_template("index.html", decks=decks)
    # else:
    #     print("Error check")

# @app.route("/deck/<deck_id>/delete", methods=["GET", "POST"])
@app.route("/deck/<deck_id>/delete", methods=["GET"])
@login_required
@roles_required('admin')
def delete_deck(deck_id):
    return render_template("remove_deck.html", deck_id=deck_id)
    # if request.method == "GET":
    #     return render_template("remove_deck.html", deck_id=deck_id)
    # elif request.method== "POST":
    #     Card.query.filter_by(deck_id=deck_id).delete()
    #     Deck.query.filter_by(deck_id=deck_id).delete()
    #     db.session.commit()
    #     decks = Deck.query.all()
    #     return render_template("index.html", decks=decks)
    # else:
    #     print("Error check")

@app.route("/deck/<deck_id>/card/create", methods=["GET"])
# @app.route("/deck/<deck_id>/card/create", methods=["GET", "POST"])
@login_required
def add_card(deck_id):
    return render_template("add_card.html", deck_id=deck_id)
    # if request.method == "GET":
    #     return render_template("add_card.html", deck_id=deck_id)
    # elif request.method== "POST":
    #     word = request.form['word'].lower()
    #     translation = request.form['translation']
    #     card = Card(deck_id=deck_id, word=word, translation=translation)
    #     db.session.add(card)
    #     db.session.commit()
    #     deck = Deck.query.filter_by(deck_id=deck_id).first()
    #     return render_template("deck.html", deck=deck)
    # else:
    #     print("Error check")


# @app.route("/deck/<deck_id>/card/search", methods=["GET"])
@app.route("/deck/<deck_id>/card/search", methods=["GET", "POST"])
def search_result(deck_id):
    # return render_template("search_word.html")
    # deck_id = request.args.get('deck')
    if request.method == "GET":
        return render_template("search_word.html", deck_id=deck_id)
    elif request.method== "POST":
        word = request.form['word'].lower()
        card = Card.query.filter(Card.deck_id==deck_id).filter(Card.word==word).first()
        # if card:
        #     deck = Deck.query.filter(Deck.deck_id==deck_id).first()
        #     deck.score += 1
        #     deck.last_review_date = func.now()
        #     db.session.commit()
        return render_template("display_word.html", deck_id=deck_id, card=card)
    else:
        print("Error check")


# @app.route("/deck/<deck_id>/card/search-result", methods=["GET"])
# def search_words(deck_id):
#     return render_template("display_word.html")


@app.route("/deck/<deck_id>/card/game", methods=["GET", "POST"])
def play_game(deck_id):
    global random_cards
    global ind
    global selected_card
    if request.method == "GET":
        random_cards = Card.query.filter(Card.deck_id==deck_id).limit(5).all()
        if random_cards:
          ind = randrange(len(random_cards))
          selected_card = random_cards[ind]
        else:
          selected_card = None
        return render_template("card_game.html", deck_id=deck_id, selected_card=selected_card, random_cards=random_cards)
    elif request.method== "POST":
        answer = request.form['answer-card'].lower()
        print(answer, selected_card.translation, selected_card.word)
        if answer == selected_card.translation:
            result = True
            deck = Deck.query.filter(Deck.deck_id==deck_id).first()
            deck.score += 1
            deck.last_review_date = func.now()
            db.session.commit()
        else:
            result = False
        return render_template("card_game_result.html", deck_id=deck_id, selected_card=selected_card, random_cards=random_cards, result=result)
    else:
        print("Error check")

@app.route("/new", methods=["GET", "POST"])
def square_check():
  # print(dir(request))
  key = int(request.args.get('key'))
  val = int(request.args.get('value'))
  if val == key*key:
    return "Matches"
  return "mismatches"

# @app.route("/hello/<user_name>", methods=["GET", "POST"])
# def hello(user_name):
#     job = tasks.hello.delay(user_name)
#     # job = tasks.hello.apply_async(user_name)
#     result = job.wait()
#     return str(result), 200
#     # return str(job), 200
