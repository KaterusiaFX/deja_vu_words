from flask import Blueprint, flash, render_template, redirect, url_for

from webapp.dictionary.forms import DictionarySearchForm
from webapp.dictionary.models import EnglishWord, FrenchWord
from webapp.user.decorators import admin_required

blueprint = Blueprint('dictionary', __name__, url_prefix='/dictionary')


@blueprint.route('/')
@admin_required
def engdict_index():
    title = "Английский словарь (в алфавитном порядке)"
    search_form = DictionarySearchForm()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    return render_template(
        'dictionary/engdict_index.html',
        page_title=title,
        english_list=english_words,
        english_list_len=english_words_sum,
        form=search_form
        )

@blueprint.route('/process-engdict-search', methods=['POST'])
def process_engdict_search():
    title = "Английский словарь (в алфавитном порядке)"
    search_form = DictionarySearchForm()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    if search_form.validate_on_submit():
        word = EnglishWord.query.filter_by(word_itself=search_form.word.data).first()
        return render_template(
            'dictionary/engdict_search.html',
            page_title=title,
            english_word=word,
            english_list_len=english_words_sum,
            form=search_form
            )

    flash('Такого слова нет в нашем английском словаре')
    return redirect(url_for('dictionary.engdict_index'))
