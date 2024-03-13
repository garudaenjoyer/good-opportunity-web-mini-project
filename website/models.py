from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

user_opportunity = db.Table('user_opportunity',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunity.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    scholarship_hours_worked = db.Column(db.Integer, default=0)
    program = db.Column(db.String(15))
    opportunities = db.relationship('Opportunity', secondary=user_opportunity, backref=db.backref('applicants', lazy='dynamic'))

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    activity = db.Column(db.String(100))
    description = db.Column(db.String(200))
    location = db.Column(db.String(100))
    time = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    hours = db.Column(db.String(10))
