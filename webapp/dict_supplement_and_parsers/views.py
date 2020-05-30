from flask import Blueprint, redirect, url_for
from flask_login import login_required

from webapp.dict_supplement_and_parsers.get_eng_words import eng_dict_generator, save_engwords_in_db
from webapp.dict_supplement_and_parsers.get_french_words import french_dict_generator, save_frenchwords_in_db
from webapp.user.decorators import admin_required
from webapp.user.models import User

blueprint = Blueprint('dict_supplement_and_parsers', __name__, url_prefix='/dict_supplement_and_parsers')


@blueprint.route('/admin_engdict_supplement/<username>')
@login_required
@admin_required
def admin_engdict_supplement(username):
    username = User.query.filter_by(username=username).first_or_404()
    engword_dict = eng_dict_generator()
    save_engwords_in_db(engword_dict)
    return redirect(url_for('dictionary.engdict_index', username=username.username))


@blueprint.route('/admin_frenchdict_supplement/<username>')
@login_required
@admin_required
def admin_frenchdict_supplement(username):
    username = User.query.filter_by(username=username).first_or_404()
    frenchword_dict = french_dict_generator()
    save_frenchwords_in_db(frenchword_dict)
    return redirect(url_for('dictionary.frenchdict_index', username=username.username))
