from database import db
from flask_login import UserMixin
from datetime import datetime

def get_hour() -> str:
    hour = datetime.now()
    formated_hour = hour.strftime('%H:%M')
    print(formated_hour)
    return formated_hour

def get_date() -> str:
    date = datetime.now()
    formated_date = date.date()
    return formated_date


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', backref='owner', lazy=True, cascade="all, delete-orphan")
    

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    total = db.Column(db.Float)
    date = db.Column(db.String, default=get_date())
    hour = db.Column(db.String, default=get_hour())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_product_owner', ondelete='CASCADE'))
