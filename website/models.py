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
    data_created = db.Column(db.DateTime(timezone= True), default= func.now())
    program = db.Column(db.String(150))
    faculty = db.Column(db.String(150))
    total_hours = db.Column(db.Integer)
    done_hours = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean(), default=False)




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
    registered_users = db.relationship('User', secondary=user_opportunity, backref=db.backref('opportunities', lazy='dynamic'))
    user_limit = db.Column(db.Integer)
