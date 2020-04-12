from flask import Blueprint, flash, redirect, render_template, session, url_for
import re

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.dictionary.dict_functions import user_engdict_search, user_frenchdict_search
from webapp.dictionary.dict_functions import user_engdict_translate, user_engdict_add_word
from webapp.dictionary.forms import EngDictionarySearchForm, FrenchDictionarySearchForm, WordInsertForm
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
        user=username.username
        )


# проблема с поиском русских слов, если два слова или через запятую, поиска по первым буквам (подсказки) тоже нет
@blueprint.route('/process-engdict-search/<username>', methods=['POST'])
@admin_required
def process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Английский словарь (в алфавитном порядке)"
    search_form = EngDictionarySearchForm()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(english_words)
    if search_form.validate_on_submit():
        word = search_form.word.data
        if re.fullmatch("[a-zA-Z]+", word):
            word = EnglishWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.fullmatch("[а-яА-Я]+", word):
            word = EnglishWord.query.filter_by(translation_rus=search_form.word.data).first()
        else:
            word = None
        if word:
            return render_template(
                'dictionary/engdict_search.html',
                page_title=title,
                english_word=word,
                english_list_len=english_words_sum,
                form=search_form,
                user=username.username
                )

        flash('Такого слова нет в нашем английском словаре')
        return redirect(url_for('.engdict_index', username=username.username))


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
        user=username.username
        )


# проблема с поиском русских слов, если два слова или через запятую, поиска по первым буквам (подсказки) тоже нет
@blueprint.route('/process-frenchdict-search/<username>', methods=['POST'])
@admin_required
def process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Французский словарь (в алфавитном порядке)"
    search_form = FrenchDictionarySearchForm()
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(french_words)
    if search_form.validate_on_submit():
        word = search_form.word.data
        if re.fullmatch("[a-zA-Z]+", word):
            word = FrenchWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.fullmatch("[а-яА-Я]+", word):
            word = FrenchWord.query.filter_by(translation_rus=search_form.word.data).first()
        else:
            word = None
        if word:
            return render_template(
                'dictionary/frenchdict_search.html',
                page_title=title,
                french_word=word,
                french_list_len=french_words_sum,
                form=search_form,
                user=username.username
                )

        flash('Такого слова нет в нашем французском словаре')
        return redirect(url_for('.frenchdict_index', username=username.username))


@blueprint.route('/user_engdict/<username>')
def user_engdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = "Ваш английский словарь"
    english_list = process_user_engdict_index(username)
    english_words_sum = len(english_list)
    return render_template(
        'dictionary/user_engdict_index.html',
        page_title=title,
        english_list=english_list,
        english_list_len=english_words_sum,
        form=search_form,
        user=username.username
        )


@blueprint.route('/user-process-engdict-search/<username>', methods=['POST'])
def user_process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Ваш английский словарь"
    search_form = EngDictionarySearchForm()
    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
        session['word'] = search_form.word.data
        word, user_english_word_status, user_english_word_date = user_engdict_search(word_in_form, username)

        if word:
            return render_template(
                'dictionary/user_engdict_search.html',
                page_title=title,
                english_word=word,
                english_word_status=user_english_word_status,
                english_word_date=user_english_word_date,
                form=search_form,
                user=username.username
                )

        flash('Такого слова нет в вашем английском словаре')
        translation = user_engdict_translate(word_in_form)
        if translation:
            translation_form = WordInsertForm()
            return render_template(
                'dictionary/user_engdict_insert.html',
                page_title=title,
                english_word=word_in_form,
                translation=translation,
                form=search_form,
                translation_form=translation_form,
                user=username.username
                )
        return redirect(url_for('.user_engdict_index', username=username.username))


@blueprint.route('/user-process-engdict-insert/<username>', methods=['POST'])
def user_process_engdict_insert(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Ваш английский словарь"
    search_form = EngDictionarySearchForm()
    form = WordInsertForm()
    word_in_form = form.insert.data
    word = session.get('word')
    english_word, translation = user_engdict_add_word(word_in_form, word, username)
    return render_template(
        'dictionary/user_engdict_insert_completed.html',
        page_title=title,
        english_word=english_word,
        translation=translation,
        form=search_form,
        user=username.username
        )


@blueprint.route('/user_frenchdict/<username>')
def user_frenchdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = "Ваш французский словарь"
    french_list = process_user_frenchdict_index(username)
    french_words_sum = len(french_list)
    return render_template(
        'dictionary/user_frenchdict_index.html',
        page_title=title,
        french_list=french_list,
        french_list_len=french_words_sum,
        form=search_form,
        user=username.username
        )


@blueprint.route('/user-process-frenchdict-search/<username>', methods=['POST'])
def user_process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Ваш французский словарь"
    search_form = FrenchDictionarySearchForm()
    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
        word, user_french_word_status, user_french_word_date = user_frenchdict_search(word_in_form, username)

        if word:
            return render_template(
                'dictionary/user_frenchdict_search.html',
                page_title=title,
                french_word=word,
                french_word_status=user_french_word_status,
                french_word_date=user_french_word_date,
                form=search_form,
                user=username.username
                )

        flash('Такого слова нет в вашем французском словаре')
        return redirect(url_for('.user_frenchdict_index', username=username.username))
