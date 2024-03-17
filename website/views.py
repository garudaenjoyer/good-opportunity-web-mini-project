from sqlalchemy import desc
from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_required, current_user, login_user
from .models import Opportunity, User
from .models import db
import json

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

@views.route('/delete_opportunity', methods= ['POST'])
def delete_oppor():
    data = json.loads(request.data)
    opporId = data['opporId']
    oppor = Opportunity.query.get(opporId)
    if oppor:
        db.session.delete(oppor)
        db.session.commit()
        flash('Opportunity was deleted', 'success')
    return jsonify({})

@views.route('/personal_cab')
@login_required
def user_page():
    # scholarship_hours_percentage = (scholarship_hours_completed / 60) * 100
    return render_template('personal_cab.html', user=current_user)
@views.route('/register_opportunity', methods= ['POST'])
def register_oppr():
    data = json.loads(request.data)
    opporId = data['opporId']
    oppor = Opportunity.query.get(opporId)
    if oppor:
        user = User.query.get(current_user.id)
        print(f"======={user.done_hours}=========")
        user.done_hours += int(oppor.hours)
        print(f"======={user.done_hours}=========")
        # db.session.delete(oppor)
        db.session.commit()
        flash('Opportunity was added', 'success')
        return jsonify({'message': 'Opportunity added successfully'}), 200
    else:
        return jsonify({'error': 'Opportunity not found'}), 404