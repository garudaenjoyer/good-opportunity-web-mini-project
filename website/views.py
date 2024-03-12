from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user, login_user
from.models import Opportunity

views = Blueprint('views', __name__)



@views.route("/")
@views.route("/home")#if just "/" goes to def home
@login_required
def home():
    opportunities = Opportunity.query.all()
    return render_template('home.html', user=current_user, admin=False, opportunities= opportunities)
