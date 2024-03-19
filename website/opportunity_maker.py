from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User, Opportunity
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

opportunity_maker = Blueprint('opportunity_maker', __name__)


@opportunity_maker.route('/secret_admin/add_opportunity', methods = ['GET', 'POST'])
def add_opportunity():
    if '/secret_admin' in request.referrer:
        if request.method == 'POST':
            date = request.form['date']
            activity = request.form['activity']
            description = request.form['description']
            location = request.form['location']
            time = request.form['time']
            email = request.form['email']
            phone = request.form['phone']
            hours = request.form['hours']
            if date and activity and description and location and time\
and email and phone and hours:
                if bool(re.match('^[a-zA-Z0-9._%+-]+@ucu\.edu\.ua$', email)) is False:
                    flash('Email shoud use "ucu.edu.ua" domain', category='error')
                if bool(re.match('^\+\d{1,3}\s?\(\d{1,3}\)\s?\d{3}-\d{2}-\d{2}$|^\+\d{9,12}$', phone)) is False:
                    flash('Incorrect phone number format', category='error')
                if int(hours) > 60:
                    flash('Hours should not exceed the value of 60', category='error')
                if int(hours) <= 0:
                    flash('Hours should be greater than zero', category='error')
                if len(description) > 1500:
                    flash('Too many symbols in description', category='error')
                if len(activity) > 150:
                    flash('Name of activity can not contain more than 150 symbols', category= 'error')
                opportunity = Opportunity(date=date, activity=activity, description=description,
                                        location=location, time=time, email=email, phone=phone, hours=hours)
                db.session.add(opportunity)
                db.session.commit()
                flash('Opportunity created successfully', 'success')
                return redirect(url_for('admin_view.admin'))
            flash('Please fill all forms', 'error')
            return redirect(url_for('admin_view.admin'))
        return render_template('add_opportunity.html', add_opportunity= True)
    else:
        abort(404)
