from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
# render-templare: able to register html templates
#redirect, url-for: for example in logout: redirects to views.home

DICT_FACUL = {
              "ПКН": "Факультет прикладних наук", 
              "ПСА": "Факультет прикладних наук", 
              "ГКУ": "Гуманітарний факультет", 
              "ГФІ": "Гуманітарний факультет", 
              "ГІС": "Гуманітарний факультет", 
              "ЗПС": "Факультет наук про здоров'я", 
              "ЗСР": "Факультет наук про здоров'я",
              "ЗПК": "Факультет наук про здоров'я",
              "ЗПП": "Факультет наук про здоров'я",
              "ЗЕР": "Факультет наук про здоров'я",
              "ЗФТ": "Факультет наук про здоров'я",
              "СЕП": "Факультет суспільних наук ",
              "СПР": "Факультет суспільних наук ",
              "ССО": "Факультет суспільних наук ",
              "СЖУ": "Факультет суспільних наук ",
              "СМЕ": "Факультет суспільних наук ",
              "СУН": "Факультет суспільних наук ",
              "СПА": "Факультет суспільних наук ",
              "СБА": "Факультет суспільних наук (ЛБШ)",
              "СІП": "Факультет суспільних наук (ЛБШ)",
              "СУМ": "Факультет суспільних наук (ЛБШ)",
              "СУП": "Факультет суспільних наук (ЛБШ)",
              "СУТ": "Факультет суспільних наук (ЛБШ)",
              "ФБА": "Філософсько-богословський факультет",
              "ФБС": "Філософсько-богословський факультет",
              "ФБК": "Філософсько-богословський факультет",
              }


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
                if user.is_admin:
                    return redirect(url_for('admin_view.admin'))
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exits', category='error')
    # if user.is_admin:
        
    return render_template('login.html', user= current_user)#, admin= False)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form_data = {
        'email': '',
        'username': '',
        'program': '',
        'total_hours': '',
        'done_hours': ''
    }

    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        program = request.form.get("program")
        total_hours = request.form.get("total_hours")
        done_hours = request.form.get("done_hours")
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        form_data = {
            'email': email,
            'username': username,
            'program': program,
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
        elif not program:
            form_data['program'] = ''
            flash('Invalid program format', category='error')

        else:
            
            new_user = User(email=email, 
                            username=username, 
                            password=generate_password_hash(password1, method='scrypt'), 
                            program=program,
                            faculty=DICT_FACUL[program[:3]],
                            total_hours=total_hours,
                            done_hours=done_hours)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user, admin=False, form_data=form_data, DICT_FACUL= DICT_FACUL)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
