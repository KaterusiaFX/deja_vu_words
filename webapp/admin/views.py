from flask import Blueprint, render_template
from webapp.user.decorators import admin_required
from flask_login import login_required

from webapp.user.models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admins')


@blueprint.route('/admin/<username>')
@login_required
@admin_required
def admin_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    return render_template('admin/admin_index.html', user=username)


