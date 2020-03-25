from flask import Blueprint, render_template
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = "Панель управления админа"
    return render_template('admin/admin_index.html', page_title=title)
