from flask import Blueprint, render_template

from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords
from webapp.user.decorators import admin_required

blueprint = Blueprint('dictionary', __name__, url_prefix='/dictionary')

@blueprint.route('/')
@admin_required
def dictionary_index():
    title = "Доступные словари сайта"
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
    return render_template(
        'dictionary/dictionary_index.html', 
        page_title=title, 
        english_list=english_words,
        english_list_len=english_words_sum, 
        french_list=french_words,
        french_list_len=french_words_sum,
        )
