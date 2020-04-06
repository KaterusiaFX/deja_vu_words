from flask import Blueprint, flash, render_template

from webapp.dictionary.forms import EngDictionarySearchForm, EngDictionarySearchFormRus
from webapp.dictionary.forms import FrenchDictionarySearchForm, FrenchDictionarySearchFormRus
from webapp.dictionary.models import EnglishWord, FrenchWord
from webapp.user.decorators import admin_required
from webapp.user.models import User

blueprint = Blueprint('dictionary', __name__, url_prefix='/dictionary')


@blueprint.route('/admin_engdict/<username>')
@admin_required
def engdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = "Английский словарь (в алфавитном порядке)"
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    return render_template(
        'dictionary/engdict_index.html',
        page_title=title,
        english_list=english_words,
        english_list_len=english_words_sum,
        form=search_form,
        user=username
        )


@blueprint.route('/admin_engdict_rus/<username>')
@admin_required
def engdict_index_rus(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchFormRus()
    title = "Английский словарь (в алфавитном порядке)"
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    return render_template(
        'dictionary/engdict_index_rus.html',
        page_title=title,
        english_list=english_words,
        english_list_len=english_words_sum,
        form=search_form,
        user=username
        )


@blueprint.route('/process-engdict-search/<username>', methods=['POST'])
def process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Английский словарь (в алфавитном порядке)"
    search_form = EngDictionarySearchForm()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    if search_form.validate_on_submit():
        word = EnglishWord.query.filter_by(word_itself=search_form.word.data).first()
        if word:
            return render_template(
                'dictionary/engdict_search.html',
                page_title=title,
                english_word=word,
                english_list_len=english_words_sum,
                form=search_form,
                user=username
                )

        flash('Такого слова нет в нашем английском словаре')
        return render_template(
            'dictionary/engdict_index.html',
            page_title=title,
            english_list=english_words,
            english_list_len=english_words_sum,
            form=search_form,
            user=username
            )


@blueprint.route('/process-engdict-search-rus/<username>', methods=['POST'])
def process_engdict_search_rus(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Английский словарь (в алфавитном порядке)"
    search_form = EngDictionarySearchFormRus()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
    if search_form.validate_on_submit():
        word = EnglishWord.query.filter_by(translation_rus=search_form.word.data).first()
        print(word)
        if word:
            return render_template(
                'dictionary/engdict_search_rus.html',
                page_title=title,
                english_word=word,
                english_list_len=english_words_sum,
                form=search_form,
                user=username
                )

        flash('Такого слова нет в нашем английском словаре')
        return render_template(
            'dictionary/engdict_index_rus.html',
            page_title=title,
            english_list=english_words,
            english_list_len=english_words_sum,
            form=search_form,
            user=username
            )


@blueprint.route('/admin_frenchdict/<username>')
@admin_required
def frenchdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = "Французский словарь (в алфавитном порядке)"
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
    return render_template(
        'dictionary/frenchdict_index.html',
        page_title=title,
        french_list=french_words,
        french_list_len=french_words_sum,
        form=search_form,
        user=username
        )


@blueprint.route('/admin_frenchdict_rus/<username>')
@admin_required
def frenchdict_index_rus(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchFormRus()
    title = "Французский словарь (в алфавитном порядке)"
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
    return render_template(
        'dictionary/frenchdict_index_rus.html',
        page_title=title,
        french_list=french_words,
        french_list_len=french_words_sum,
        form=search_form,
        user=username
        )


@blueprint.route('/process-frenchdict-search/<username>', methods=['POST'])
def process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Французский словарь (в алфавитном порядке)"
    search_form = FrenchDictionarySearchForm()
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
    if search_form.validate_on_submit():
        word = FrenchWord.query.filter_by(word_itself=search_form.word.data).first()
        if word:
            return render_template(
                'dictionary/frenchdict_search.html',
                page_title=title,
                french_word=word,
                french_list_len=french_words_sum,
                form=search_form,
                user=username
                )

        flash('Такого слова нет в нашем французском словаре')
        return render_template(
            'dictionary/frenchdict_index.html',
            page_title=title,
            french_list=french_words,
            french_list_len=french_words_sum,
            form=search_form,
            user=username
            )


@blueprint.route('/process-frenchdict-search-rus/<username>', methods=['POST'])
def process_frenchdict_search_rus(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Французский словарь (в алфавитном порядке)"
    search_form = FrenchDictionarySearchFormRus()
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
    if search_form.validate_on_submit():
        word = FrenchWord.query.filter_by(translation_rus=search_form.word.data).first()
        if word:
            return render_template(
                'dictionary/frenchdict_search_rus.html',
                page_title=title,
                french_word=word,
                french_list_len=french_words_sum,
                form=search_form,
                user=username
                )

        flash('Такого слова нет в нашем французском словаре')
        return render_template(
            'dictionary/frenchdict_index_rus.html',
            page_title=title,
            french_list=french_words,
            french_list_len=french_words_sum,
            form=search_form,
            user=username
            )
