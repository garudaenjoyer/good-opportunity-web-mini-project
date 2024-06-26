from sqlalchemy import desc
from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify, abort
from flask_login import login_required, current_user, login_user
from .models import Opportunity, User
from .models import db
import json

views = Blueprint('views', __name__)



@views.route("/")
@views.route("/home")#if just "/" goes to def home
@login_required
def home():
    # if current_user.is_admin:
    #     abort(404)
    filter_key = request.args.get('filter_key')
    if filter_key == "old":
        opportunities = Opportunity.query.order_by(Opportunity.date).all()
    elif filter_key == "new":
        opportunities = Opportunity.query.order_by(desc(Opportunity.date)).all()
    elif filter_key      == "amount":
        opportunities = Opportunity.query.order_by(desc(Opportunity.hours)).all()
    else:
        opportunities = Opportunity.query.all()

    return render_template('home.html', user=current_user, admin=False, opportunities= opportunities, len=len)

@views.route('/delete_opportunity', methods= ['POST'])
def delete_oppor():
    data = json.loads(request.data)
    opporId = data['opporId']
    oppor = Opportunity.query.get(opporId)
    if oppor:
        db.session.delete(oppor)
        db.session.commit()
        flash('Можливість успішно видалена', 'success')
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
        if user not in oppor.registered_users and len(oppor.registered_users) < oppor.user_limit:
            oppor.registered_users.append(user)
            print(oppor.registered_users)
            db.session.commit()
            flash('Ви успішно зареєструвались на можливість', 'success')
            return jsonify({'message': 'Opportunity added successfully'}), 200
        elif user in oppor.registered_users:
            flash('Ви вже зареєстровані на цю можливість', 'error')
            print(oppor.registered_users)
            return jsonify({'error': 'Ви вже зареєстровані на цю можливість'}), 404
        else:
            flash('Вже набрана потрібна кількість людей', 'error')
            print(oppor.registered_users)
            return jsonify({'error': 'Вже набрана потрібна кількість людей'}), 404
    else:
        return jsonify({'error': 'Немає такої можливості'}), 404


@views.route('/registered_users/<int:opportunity_id>')
def all_registered_users(opportunity_id):
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    users = opportunity.registered_users
    return render_template('all_users.html', user = current_user,admin=True, users=users, opportunity=opportunity)

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