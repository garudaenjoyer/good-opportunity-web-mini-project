from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# render-templare: able to register html templates
#redirect, url-for: for example in logout: redirects to views.home

DICT_FACUL = {"ПКН": "Факультет прикладних наук", 
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
              "ФБА": "Філософсько-богословський факультет",
              "ФБС": "Філософсько-богословський факультет",
              "ФБК": "Філософсько-богословський факультет",
              }


auth = Blueprint('auth', __name__)



#by default, method is get, but we extended it to get and post
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

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        #using request, getting into form, and getting username
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        program = request.form.get("facultprogram")
        total_hours = int(request.form.get("total_time"))
        done_hours = int(request.form.get("done_hours"))
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email already exists', category='error')
        elif username_exists:
            flash('Username already exists', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        elif total_hours > 60:
            flash(f'{total_hours} is to many', category='error')
        else:
            #else create user
            new_user = User(email= email, 
                            username= username, 
                            password = generate_password_hash(password1, method='scrypt'), 
                            program = program,
                            faculty =  DICT_FACUL[program[:3]],
                            total_hours = total_hours,
                            done_hours = done_hours)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('sign-up.html', user= current_user, admin= False)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
