from flask import Blueprint, flash, render_template
import re

from webapp.dictionary.forms import EngDictionarySearchForm, FrenchDictionarySearchForm
from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, UsersWords
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


# проблема с поиском русских слов, если два слова или через запятую, поиска по первым буквам (подсказки) тоже нет
@blueprint.route('/process-engdict-search/<username>', methods=['POST'])
@admin_required
def process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Английский словарь (в алфавитном порядке)"
    search_form = EngDictionarySearchForm()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(EnglishWord.query.order_by(EnglishWord.word_itself).all())
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


# проблема с поиском русских слов, если два слова или через запятую, поиска по первым буквам (подсказки) тоже нет
@blueprint.route('/process-frenchdict-search/<username>', methods=['POST'])
@admin_required
def process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = "Французский словарь (в алфавитном порядке)"
    search_form = FrenchDictionarySearchForm()
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(FrenchWord.query.order_by(FrenchWord.word_itself).all())
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
        if user_word.user_engword_id:
            eng_word = EnglishWordOfUser.query.filter_by(id=user_word.user_engword_id).first()
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
        user=username
        )


@blueprint.route('/user-process-engdict-search/<username>', methods=['POST'])
def user_process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = username.id
    title = "Ваш английский словарь"
    search_form = EngDictionarySearchForm()
    user_words = UsersWords.query.filter_by(user_id=user_id).all()

    english_words, english_words_status, english_words_date = [], [], []
    for user_word in user_words:
        if user_word.engword_id:
            eng_word = EnglishWord.query.filter_by(id=user_word.engword_id).first()
        if user_word.user_engword_id:
            eng_word = EnglishWordOfUser.query.filter_by(id=user_word.user_engword_id).first()
        english_words.append(eng_word)
        english_words_status.append(user_word.status)
        english_words_date.append(user_word.imported_time)
    english_list = list(zip(english_words, english_words_status, english_words_date))
    english_words_sum = len(english_list)

    if search_form.validate_on_submit():
        word = search_form.word.data
        word_exist_userdict = EnglishWordOfUser.query.filter_by(word_itself=word).all()
        word_exist = EnglishWord.query.filter_by(word_itself=word).first()
        if re.match("[a-zA-Z]+", word):
            for userword in user_words:
                if word_exist and userword.engword_id == word_exist.id:
                    word = word_exist
                    user_english_word_status, user_english_word_date = userword.status, userword.imported_time
                elif word_exist_userdict:
                    for every_word in word_exist_userdict:
                        if every_word.user == username and every_word.id == userword.user_engword_id:
                            word = every_word
                            user_english_word_status, user_english_word_date = userword.status, userword.imported_time
        else:
            word = None
        if word:
            return render_template(
                'dictionary/user_engdict_search.html',
                page_title=title,
                english_word=word,
                english_word_status=user_english_word_status,
                english_word_date=user_english_word_date,
                english_list_len=english_words_sum,
                form=search_form,
                user=username
                )

        flash('Такого слова нет в нашем английском словаре')
        return render_template(
            'dictionary/user_engdict_index.html',
            page_title=title,
            english_list=english_words,
            english_list_len=english_words_sum,
            form=search_form,
            user=username
            )
