from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User, Opportunity
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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
                opportunity = Opportunity(date=date, activity=activity, description=description,
                                        location=location, time=time, email=email, phone=phone, hours=hours)
                db.session.add(opportunity)
                db.session.commit()
                flash('Opportunity created successfully', 'success')
                return redirect(url_for('admin_view.admin'))
            flash('Please fill all forms', 'error')
            return redirect(url_for('admin_view.admin'))
        return render_template('add_opportunity.html', add_opportunity=True, user=current_user, admin = True)
    else:
        abort(404)

@opportunity_maker.route('/generate_dummy_opportunities', methods=['GET'])
@login_required
def generate_dummy_opportunities():
    dummy_opportunities = [
        {
    'date': '2024-03-16',
    'activity': 'Community Cleanup Day',
    'description': 'Join us for a community cleanup event to beautify our neighborhood and promote environmental stewardship. Volunteers will receive a free lunch and a certificate of appreciation.',
    'location': 'Central Park',
    'time': '9:00 AM - 12:00 PM',
    'email': 'volunteer@communitycleanup.org',
    'phone': '555-123-4567',
    'hours': '4'
},
{
    'date': '2024-03-20',
    'activity': 'Children\'s Book Reading',
    'description': 'Share the joy of reading with children at the local library. Volunteers will read stories to kids and help them discover the magic of books.',
    'location': 'City Library',
    'time': '10:00 AM - 11:30 AM',
    'email': 'reading@library.org',
    'phone': '555-987-6543',
    'hours': '2'
},
{
    'date': '2024-03-25',
    'activity': 'Food Drive',
    'description': 'Collect non-perishable food items for families in need. Help make a difference in the community by contributing to this important cause.',
    'location': 'Community Center',
    'time': '2:00 PM - 4:00 PM',
    'email': 'fooddrive@communitycenter.org',
    'phone': '555-789-0123',
    'hours': '3'
},
{
    'date': '2024-03-30',
    'activity': 'Senior Center Visit',
    'description': 'Spend time with seniors at the local senior center. Engage in conversations, play games, and bring smiles to their faces.',
    'location': 'Senior Center',
    'time': '1:30 PM - 3:30 PM',
    'email': 'seniors@seniorcenter.org',
    'phone': '555-321-6548',
    'hours': '2'
},
{
    'date': '2024-04-05',
    'activity': 'Park Cleanup',
    'description': 'Help clean up litter and maintain the beauty of our local park. Gloves and trash bags will be provided. All ages welcome!',
    'location': 'City Park',
    'time': '9:00 AM - 11:00 AM',
    'email': 'parkcleanup@citypark.org',
    'phone': '555-456-7890',
    'hours': '2'
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
            hours=data['hours']
        )
        db.session.add(opportunity)
    
    db.session.commit()
    flash('Dummy opportunities created successfully', 'success')
    return redirect(url_for('views.home'))
    