from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user, login_user
from .models import Opportunity
from sqlalchemy import desc

views = Blueprint('views', __name__)



@views.route("/")
@views.route("/home")#if just "/" goes to def home
@login_required
def home():
    filter_key = request.args.get('filter_key')
    if filter_key == "old":
        opportunities = Opportunity.query.order_by(Opportunity.date).all()
    elif filter_key == "new":
        opportunities = Opportunity.query.order_by(desc(Opportunity.date)).all()
    elif filter_key == "amount":
        opportunities = Opportunity.query.order_by(desc(Opportunity.hours)).all()
    else:
        opportunities = Opportunity.query.all()

    return render_template('home.html', user=current_user, admin=False, opportunities= opportunities)
