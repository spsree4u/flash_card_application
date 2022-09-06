from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin

from application.database import db


roles_users = db.Table('roles_users', 
                      db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')), 
                      db.Column('role_id', db.Integer, db.ForeignKey('role.role_id')))


class Deck(db.Model):
    __tablename__ = 'deck'
    deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    last_review_date = db.Column(db.DateTime, nullable=False, default=func.now())
    score = db.Column(db.Integer, default=0)

class Card(db.Model):
    __tablename__ = 'card'
    # card_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.deck_id"), nullable=False, primary_key=True)
    word = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
