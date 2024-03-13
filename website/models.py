from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


#database, row: new user, column: user_info
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(150), unique= True)
    username = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    data_created = db.Column(db.DateTime(timezone= True), default= func.now())
    faculty = db.Column(db.String(150))
    total_hours = db.Column(db.Integer)
    done_hours = db.Column(db.Integer)

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
    