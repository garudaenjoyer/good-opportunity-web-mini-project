from flask import Blueprint, render_template, url_for, redirect
from .models import Opportunity


admin_views = Blueprint('admin_view', __name__)


@admin_views.route('/secret_admin')
def admin():
    opportunities = Opportunity.query.all()
    return render_template('home.html', admin=True, opportunities= opportunities)
