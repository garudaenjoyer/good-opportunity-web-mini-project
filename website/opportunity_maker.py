from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User, Opportunity
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

opportunity_maker = Blueprint('opportunity_maker', __name__)


@opportunity_maker.route('/admin/add_opportunity', methods=['GET', 'POST'])
def add_opportunity():
    form_data = {
        'date': '',
        'activity': '',
        'description': '',
        'location': '',
        'time': '',
        'email': '',
        'phone': '',
        'hours': '',
        'limit': ''
    }
    if request.referrer and '/admin' in request.referrer:
        if request.method == 'POST':
            date = request.form['date']
            activity = request.form['activity']
            description = request.form['description']
            location = request.form['location']
            time = request.form['time']
            email = request.form['email']
            phone = request.form['phone']
            hours = request.form['hours']
            limit = int(request.form['limit'])

            form_data = {
                'date': date,
                'activity': activity,
                'description': description,
                'location': location,
                'time': time,
                'email': email,
                'phone': phone,
                'hours': hours,
                'limit': limit
            }

            if bool(re.match('^[a-zA-Z0-9._%+-]+@ucu\.edu\.ua$', email)) is False:
                flash('Email should use "ucu.edu.ua" domain', category='error')
                form_data['email'] = ''

            elif bool(re.match("^\+\d{1,2}( \()?\d{1,3}(\) )?\d{3}-?\d{2}-?\d{2}$", phone)) is False:
                flash('Incorrect phone number format', category='error')
                form_data['phone'] = ''

            elif int(hours) > 60:
                flash('Hours should not exceed the value of 60', category='error')
                form_data['hours'] = ''
            elif int(hours) <= 0:
                flash('Hours should be greater than zero', category='error')
                form_data['hours'] = ''

            elif len(description) > 1500:
                flash('Too many symbols in description', category='error')
                form_data['description'] = ''

            elif len(activity) > 150:
                flash('Name of activity cannot contain more than 150 symbols', category='error')
                form_data['activity'] = ''

            else:
                opportunity = Opportunity(date=date, activity=activity, description=description,
                                          location=location, time=time, email=email, phone=phone, hours=hours,
                                          user_limit=limit)
                db.session.add(opportunity)
                db.session.commit()
                flash('Opportunity created successfully', 'success')
                return redirect(url_for('admin_view.admin'))
            # Return the rendered template with form_data to preserve entered values
            return render_template('add_opportunity.html', add_opportunity=True, user=current_user, admin=True,
                                   form_data=form_data)
        return render_template('add_opportunity.html', add_opportunity=True, user=current_user, admin=True,
                               form_data=form_data)
    abort(404)


@opportunity_maker.route('/generate_dummy_opportunities', methods=['GET'])
@login_required
def generate_dummy_opportunities():
    dummy_opportunities = [
        {
            'date': '2024-03-16',
            'activity': 'Community Cleanup Day',
            'description': 'Join us for a community cleanup event to beautify our neighborhood and promote '
                           'environmental stewardship. Volunteers will receive a free lunch and a certificate of '
                           'appreciation.',
            'location': 'Central Park',
            'time': '9:00 AM - 12:00 PM',
            'email': 'volunteer@communitycleanup.org',
            'phone': '555-123-4567',
            'hours': '4',
            'limit': '3'
        },
        {
            'date': '2024-03-20',
            'activity': 'Children\'s Book Reading',
            'description': 'Share the joy of reading with children at the local library. Volunteers will read '
                           'stories to kids and help them discover the magic of books.',
            'location': 'City Library',
            'time': '10:00 AM - 11:30 AM',
            'email': 'reading@library.org',
            'phone': '555-987-6543',
            'hours': '2',
            'limit': '3'
        },
        {
            'date': '2024-03-25',
            'activity': 'Food Drive',
            'description': 'Collect non-perishable food items for families in need. Help make a difference in the '
                           'community by contributing to this important cause.',
            'location': 'Community Center',
            'time': '2:00 PM - 4:00 PM',
            'email': 'fooddrive@communitycenter.org',
            'phone': '555-789-0123',
            'hours': '3',
            'limit': '3'
        },
        {
            'date': '2024-03-30',
            'activity': 'Senior Center Visit',
            'description': 'Spend time with seniors at the local senior center. Engage in conversations, play games, '
                           'and bring smiles to their faces.',
            'location': 'Senior Center',
            'time': '1:30 PM - 3:30 PM',
            'email': 'seniors@seniorcenter.org',
            'phone': '555-321-6548',
            'hours': '2',
            'limit': '3'
        },
        {
            'date': '2024-04-05',
            'activity': 'Park Cleanup',
            'description': 'Help clean up litter and maintain the beauty of our local park. Gloves and trash bags will '
                           'be provided. All ages welcome!',
            'location': 'City Park',
            'time': '9:00 AM - 11:00 AM',
            'email': 'parkcleanup@citypark.org',
            'phone': '555-456-7890',
            'hours': '2',
            'limit': '3'
        }
    ]

    for data in dummy_opportunities:
        opportunity = Opportunity(
            date=data['date'],
            activity=data['activity'],
            description=data['description'],
            location=data['location'],
            time=data['time'],
            email=data['email'],
            phone=data['phone'],
            hours=data['hours'],
            user_limit=data['limit']
        )
        db.session.add(opportunity)

    db.session.commit()
    flash('Dummy opportunities created successfully', 'success')
    return redirect(url_for('views.home'))
