from flask import Blueprint, render_template, url_for, redirect, abort
from .models import Opportunity
from flask_login import login_required, current_user


admin_views = Blueprint('admin_view', __name__)


@admin_views.route('/admin')
@login_required
def admin():
    # user = 
    if current_user.is_admin:
        opportunities = Opportunity.query.all()
        return render_template('home.html', admin=current_user.is_admin, opportunities= opportunities)
    abort(404)
