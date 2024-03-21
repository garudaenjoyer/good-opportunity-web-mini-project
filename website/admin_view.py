from flask import Blueprint, render_template, url_for, redirect, abort, request
from .models import Opportunity
from flask_login import login_required, current_user
from sqlalchemy import desc

admin_views = Blueprint("admin_view", __name__)


@admin_views.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        abort(404)
    filter_key = request.args.get("filter_key")
    if filter_key == "old":
        opportunities = Opportunity.query.order_by(Opportunity.date).all()
    elif filter_key == "new":
        opportunities = Opportunity.query.order_by(desc(Opportunity.date)).all()
    elif filter_key == "amount":
        opportunities = Opportunity.query.order_by(desc(Opportunity.hours)).all()
    else:
        opportunities = Opportunity.query.all()
    return render_template(
        "home.html", admin=current_user.is_admin, opportunities=opportunities
    )
