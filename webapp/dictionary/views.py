from flask import Blueprint, flash, redirect, render_template, url_for
import re

from webapp.dictionary.dict_functions import user_engdict_search
from webapp.dictionary.forms import EngDictionarySearchForm, FrenchDictionarySearchForm
from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords
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
        if re.match("[a-zA-Z]+", word):
            word = EnglishWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.match("[а-яА-Я]+", word):
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
        if re.match("[a-zA-Z]+", word):
            word = FrenchWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.match("[а-яА-Я]+", word):
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
    user_id = username.id
    search_form = EngDictionarySearchForm()
    title = "Ваш английский словарь"
    user_words = UsersWords.query.filter_by(user_id=user_id).all()

    english_words, english_words_status, english_words_date = [], [], []
    for user_word in user_words:
        if user_word.engword_id:
            eng_word = EnglishWord.query.filter_by(id=user_word.engword_id).first()
        elif user_word.user_engword_id:
            eng_word = EnglishWordOfUser.query.filter_by(id=user_word.user_engword_id).first()
        else:
            eng_word = None
        if eng_word:
            english_words.append(eng_word)
            english_words_status.append(user_word.status)
            english_words_date.append(user_word.imported_time)
    english_list = list(zip(english_words, english_words_status, english_words_date))
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
    user_id = username.id
    title = "Ваш английский словарь"
    search_form = EngDictionarySearchForm()

    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
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
        return redirect(url_for('.user_engdict_index', username=username.username))


@blueprint.route('/user_frenchdict/<username>')
def user_frenchdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = username.id
    search_form = FrenchDictionarySearchForm()
    title = "Ваш французский словарь"
    user_words = UsersWords.query.filter_by(user_id=user_id).all()

    french_words, french_words_status, french_words_date = [], [], []
    for user_word in user_words:
        if user_word.frenchword_id:
            french_word = FrenchWord.query.filter_by(id=user_word.frenchword_id).first()
        elif user_word.user_frenchword_id:
            french_word = FrenchWordOfUser.query.filter_by(id=user_word.user_frenchword_id).first()
        else:
            french_word = None
        if french_word:
            french_words.append(french_word)
            french_words_status.append(user_word.status)
            french_words_date.append(user_word.imported_time)
    french_list = list(zip(french_words, french_words_status, french_words_date))
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
    user_id = username.id
    title = "Ваш французский словарь"
    search_form = FrenchDictionarySearchForm()
    user_words = UsersWords.query.filter_by(user_id=user_id).all()

    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
        if re.match("[a-zA-Z]+", word_in_form):
            word_exist_userdict = FrenchWordOfUser.query.filter_by(word_itself=word_in_form).all()
            word_exist = FrenchWord.query.filter_by(word_itself=word_in_form).first()
            for userword in user_words:
                if word_exist and userword.frenchword_id == word_exist.id:
                    word = word_exist
                    user_french_word_status, user_french_word_date = userword.status, userword.imported_time
                elif word_exist_userdict:
                    for every_word in word_exist_userdict:
                        if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                            word = every_word
                            user_french_word_status, user_french_word_date = userword.status, userword.imported_time
        elif re.match("[а-яА-Я]+", word_in_form):
            word_exist_userdict = FrenchWordOfUser.query.filter_by(translation_rus=word_in_form).all()
            word_exist = FrenchWord.query.filter_by(translation_rus=word_in_form).first()
            for userword in user_words:
                if word_exist and userword.frenchword_id == word_exist.id:
                    word = word_exist
                    user_french_word_status, user_french_word_date = userword.status, userword.imported_time
                elif word_exist_userdict:
                    for every_word in word_exist_userdict:
                        if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                            word = every_word
                            user_french_word_status, user_french_word_date = userword.status, userword.imported_time
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
