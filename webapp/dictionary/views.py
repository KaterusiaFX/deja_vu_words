from flask import Blueprint, render_template

from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords
from webapp.user.decorators import admin_required

blueprint = Blueprint('dictionary', __name__, url_prefix='/dictionary')

@blueprint.route('/')
@admin_required
def dictionary_index():
    title = "Общий словарь на сайте"
    return render_template('dictionary/dictionary_index.html', page_title=title)
