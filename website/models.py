from datetime import datetime, timezone
from sqlalchemy.sql.elements import False_
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%d')
        return value


class Note(db.Model):
    ''' Make these notes posts later! (And maybe add a title too)'''
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    # Make sure the following is date with an 'e' and not an 'a'! The time is in the time of the gps timezone so for us CET.
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())

    # Get the user id out of the database part of the user, foreign keys use lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='notes')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 150 is the max String length, and it should be an unique email
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(MyDateTime)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    # The notes that a user has created, use for relationships a capital
    notes = db.relationship('Note', back_populates='user')
