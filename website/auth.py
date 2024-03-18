from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
# render-templare: able to register html templates
#redirect, url-for: for example in logout: redirects to views.home
auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email= email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exits', category='error')
    return render_template('login.html', user= current_user, admin= False)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form_data = {
        'email': '',
        'username': '',
        'faculty': '',
        'total_hours': '',
        'done_hours': ''
    }

    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        faculty = request.form.get("faculty")
        total_hours = request.form.get("total_hours")
        done_hours = request.form.get("done_hours")
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        form_data = {
            'email': email,
            'username': username,
            'faculty': faculty,
            'total_hours': total_hours,
            'done_hours': done_hours
        }

        if email_exists:
            flash('Email already exists', category='error')
            form_data['email'] = ''
        elif not re.match('^[a-zA-Z0-9._%+-]+@ucu\.edu\.ua$', email):
            flash('Email should use "ucu.edu.ua" domain', category='error')
            form_data['email'] = ''
        elif username_exists:
            flash('Username already exists', category='error')
            form_data['username'] = ''
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            form_data['username'] = ''
            flash('Username is too short', category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        elif not total_hours:
            form_data['total_hours'] = ''
            flash('You forgot to fill in total hours', category='error')
        elif int(total_hours) > 60:
            form_data['total_hours'] = ''
            flash('Total hours cannot exceed 60', category='error')
        elif not done_hours:
            flash('You forgot to fill in done hours', category='error')
        elif not re.match('^[А-Я]{3}\d{2}/[А-Я]$', faculty):
            form_data['faculty'] = ''
            flash('Invalid faculty format', category='error')

        else:
            try:
                total_hours = int(total_hours)
            except ValueError:
                total_hours = 60

            try:
                done_hours = int(done_hours)
            except ValueError:
                done_hours = 0

            new_user = User(email=email, 
                            username=username, 
                            password=generate_password_hash(password1, method='scrypt'), 
                            faculty=faculty,
                            total_hours=total_hours,
                            done_hours=done_hours)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user, admin=False, form_data=form_data)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
