
import os
import pandas as pd
from datetime import datetime
from celery.schedules import crontab
from flask import current_app as app

from application.workers import celery
from application.utils import format_email_message, send_email
from application.models import User, Deck, Card


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10, hello.s(), name="At every 10 seconds")
    sender.add_periodic_task(crontab(), send_daily_reminder.s(), name="Daily reminder!!")
    # sender.add_periodic_task(crontab(minute=37, hour=20), hello.s(), name="Daily reminder!!")
    sender.add_periodic_task(crontab(), send_monthly_report.s(), name="Monthly progress report!!")
    sender.add_periodic_task(crontab(), send_decks_cards_report.s(), name="Decks cards report!!")

@celery.task()
def send_daily_reminder():
    reminder_template = os.path.join(app.config["TEMPLATE_DIR_PATH"], "daily_notification.html")
    attachment = os.path.join(app.config["DOCS_DIR_PATH"], "Flash Card Application Helper.pdf")
    users = User.query.all()
    for user in users:
        message = format_email_message(reminder_template, data={"name": user.username})
        send_email(to=user.email, subject='FCA Review Reminder', message=message, content="html", attachment=attachment)

@celery.task()
def send_monthly_report():
    reminder_template = os.path.join(app.config["TEMPLATE_DIR_PATH"], "monthly_progress_report.html")

    decks = Deck.query.all()
    deck_scores = [{"deck_name": deck.title, "deck_score": deck.score} for deck in decks]

    users = User.query.all()
    for user in users:
        message = format_email_message(reminder_template, user={"name": user.username}, deck_scores=deck_scores)
        send_email(to=user.email, subject='FCA Monthly Progress Report', message=message, content="html")

@celery.task()
def send_decks_cards_report():
    reminder_template = os.path.join(app.config["TEMPLATE_DIR_PATH"], "decks_cards_report_notification.html")

    decks = Deck.query.all()
    deck_scores = [{"deck_name": deck.title, "deck_score": deck.score} for deck in decks]
    decks_cards_list = []
    for deck in decks:
        cards = Card.query.filter(Card.deck_id==deck.deck_id).all()
        for card in cards:
            decks_cards_list.append([deck.title, card.word, card.translation])

    df = pd.DataFrame(decks_cards_list, columns=["Deck", "Card", "Meaning"])
    attachment = os.path.join(app.config["DOCS_DIR_PATH"], "decks_cards_report.csv")
    df.to_csv(attachment, index=False)

    users = User.query.all()
    for user in users:
        message = format_email_message(reminder_template, data={"name": user.username})
        send_email(to=user.email, subject='FCA Decks Cards Report', message=message, content="html", attachment=attachment)