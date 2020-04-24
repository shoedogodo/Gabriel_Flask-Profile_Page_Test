from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), default="")
    age = db.Column(db.String(1000), default="")
    favorite_word = db.Column(db.String(1000), default="")
    log_in_count = db.Column(db.Integer, default=0)
    pic = db.Column(db.String(100000))
