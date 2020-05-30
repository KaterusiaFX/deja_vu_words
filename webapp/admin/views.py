from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from webapp.db import db
from webapp.user.decorators import admin_required
from webapp.user.forms import RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admins')


@blueprint.route('/admin/<username>')
@login_required
@admin_required
def admin_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    return render_template('admin/admin_index.html', user=username)


@blueprint.route('/users_management/<username>')
@login_required
@admin_required
def users_management(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Управление пользователями'
    all_users = User.query.order_by(User.role).all()
    return render_template(
        'admin/users_management.html',
        page_title=title,
        all_users=all_users,
        user=username
        )


@blueprint.route('/register_admin/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def register_admin(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Регистрация нового админа'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role='admin')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Новый админ успешно зарегистрирован!')
        return redirect(url_for('admin.users_management', username=username.username))
    return render_template('admin/register_admin.html', page_title=title, form=form)
