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
        if user not in oppor.registered_users:
            # print(f"======={user.done_hours}=========")
            # user.done_hours += int(oppor.hours)
            # print(f"======={user.done_hours}=========")
            # # db.session.delete(oppor)
            oppor.registered_users.append(user)
            print(oppor.registered_users)
            db.session.commit()
            flash('You were registered', 'success')
            return jsonify({'message': 'Opportunity added successfully'}), 200
        else:
            flash('You have already registered', 'success')
            print(oppor.registered_users)
            return jsonify({'error': 'You have already registered'}), 404
    else:
        return jsonify({'error': 'Opportunity not found'}), 404
    

@views.route('/registered_users/<int:opportunity_id>')
def all_registered_users(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    users = opportunity.registered_users
    return render_template('all_users.html', users=users, opportunity=opportunity)

@views.route('/process_users/<int:opportunity_id>', methods=['POST'])
def process_users(opportunity_id):
    selected_user_ids = request.form.getlist('user_ids')  # Get list of selected user IDs
    opportunity_hours = request.args.get('hours', 0)   # Get opportunity hours
    selected_users = User.query.filter(User.id.in_(selected_user_ids)).all()
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    for user in selected_users:
        user.done_hours += int(opportunity_hours)
        opportunity.registered_users.pop(opportunity.registered_users.index(user))
    db.session.commit()
    return redirect(url_for('admin_view.admin'))