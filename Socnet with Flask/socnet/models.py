from app import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(40))
    login = db.Column(db.String(15))
    password = db.Column(db.String(20))
    email = db.Column(db.String(40))
    birthday = db.Column(db.DateTime, default=None)
    gender = db.Column(db.String(10), default=None)
    avatar = db.Column(db.String(60), default="user.png")
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, firstname, lastname, login, password, email, gender):
        self.firstname = firstname
        self.lastname = lastname
        self.login = login
        self.password = password
        self.email = email
        self.gender = gender


class Photos(db.Model):
    __tablename__ = "photos"
    photos_id = db.Column("photos_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # avelacnoxi aydin
    photo_name = db.Column(db.Text())  # nkari anunn
    like = db.Column(db.Integer, default=0)

    def __init__(self, user_id, photo_name, like=0):
        self.user_id = user_id
        self.photo_name = photo_name
        self.like = like


class Friends(db.Model):
    __tablename_ = "friends"
    friend_id = db.Column("friend_id", db.Integer, primary_key=True)
    user_1 = db.Column(db.Integer)
    user_2 = db.Column(db.Integer)

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2


class Messages(db.Model):
    __tablename__ = "messages"
    message_id = db.Column("message_id", db.Integer, primary_key=True)
    user_1 = db.Column(db.Integer)
    user_2 = db.Column(db.Integer)
    message = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_1, user_2, message):
        self.user_1 = user_1
        self.user_2 = user_2
        self.message = message


class Requests(db.Model):
    __tablename__ = "requests"
    request_id = db.Column("request_id", db.Integer, primary_key=True)
    user_1 = db.Column(db.Integer)
    user_2 = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2


db.create_all()
