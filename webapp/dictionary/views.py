import re

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.dictionary.dict_functions import user_engdict_search, user_frenchdict_search
from webapp.dictionary.dict_functions import user_engdict_translate, user_frenchdict_translate
from webapp.dictionary.dict_functions import user_engdict_add_word, user_frenchdict_add_word
from webapp.dictionary.dict_functions import user_engdict_delete_word, user_frenchdict_delete_word
from webapp.dictionary.forms import BackToEngDictionary, BackToFrenchDictionary
from webapp.dictionary.forms import DeleteEngWordButton, DeleteFrenchWordButton
from webapp.dictionary.forms import EngDictionarySearchForm, FrenchDictionarySearchForm, WordInsertForm
from webapp.dictionary.models import EnglishWord, FrenchWord
from webapp.user.decorators import admin_required
from webapp.user.models import User
from webapp.user.views import check_teacher_student

blueprint = Blueprint('dictionary', __name__, url_prefix='/dictionary')


@blueprint.route('/admin_engdict/<username>')
@admin_required
def engdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = 'Английский словарь (в алфавитном порядке)'
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


# a problem with the search for Russian words, if two words or separated by commas,
# there is no search in the first letters (hints) either
@blueprint.route('/process-engdict-search/<username>', methods=['POST'])
@admin_required
def process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Английский словарь (в алфавитном порядке)'
    search_form = EngDictionarySearchForm()
    english_words = EnglishWord.query.order_by(EnglishWord.word_itself).all()
    english_words_sum = len(english_words)
    if search_form.validate_on_submit():
        word = search_form.word.data
        if re.fullmatch('[a-zA-Z- ]+', word):
            word = EnglishWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.fullmatch('[а-яА-Я- ]+', word):
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
    title = 'Французский словарь (в алфавитном порядке)'
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


# a problem with the search for Russian words, if two words or separated by commas,
# there is no search in the first letters (hints) either
@blueprint.route('/process-frenchdict-search/<username>', methods=['POST'])
@admin_required
def process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Французский словарь (в алфавитном порядке)'
    search_form = FrenchDictionarySearchForm()
    french_words = FrenchWord.query.order_by(FrenchWord.word_itself).all()
    french_words_sum = len(french_words)
    if search_form.validate_on_submit():
        word = search_form.word.data
        if re.fullmatch('[a-zA-ZÀ-ÿÆæŒœ -]+', word):
            word = FrenchWord.query.filter_by(word_itself=search_form.word.data).first()
        elif re.fullmatch('[а-яА-Я- ]+', word):
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
    title = 'Ваш английский словарь'
    english_list = process_user_engdict_index(username)
    english_words_sum = len(english_list)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_engdict_index.html',
        page_title=title,
        english_list=english_list,
        english_list_len=english_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_engdict_new/<username>')
def user_engdict_index_new(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = 'Ваш английский словарь'
    english_list = process_user_engdict_index(username)
    english_list_new = [word for word in english_list if word[1] == 'new']
    english_words_sum = len(english_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_engdict_index_new.html',
        page_title=title,
        english_list=english_list_new,
        english_list_len=english_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_engdict_familiar/<username>')
def user_engdict_index_familiar(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = 'Ваш английский словарь'
    english_list = process_user_engdict_index(username)
    english_list_new = [word for word in english_list if word[1] == 'familiar']
    english_words_sum = len(english_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_engdict_index_familiar.html',
        page_title=title,
        english_list=english_list_new,
        english_list_len=english_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_engdict_forgotten/<username>')
def user_engdict_index_forgotten(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = EngDictionarySearchForm()
    title = 'Ваш английский словарь'
    english_list = process_user_engdict_index(username)
    english_list_new = [word for word in english_list if word[1] == 'forgotten']
    english_words_sum = len(english_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_engdict_index_forgotten.html',
        page_title=title,
        english_list=english_list_new,
        english_list_len=english_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user-process-engdict-search/<username>', methods=['POST'])
def user_process_engdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Ваш английский словарь'
    search_form = EngDictionarySearchForm()
    delete_form = DeleteEngWordButton()
    back_form = BackToEngDictionary()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
        session['word'] = search_form.word.data
        word, user_english_word_status, user_english_word_date, userword_id = user_engdict_search(
            word_in_form,
            username
            )

        if word:
            return render_template(
                'dictionary/user_engdict_search.html',
                page_title=title,
                english_word=word,
                english_word_status=user_english_word_status,
                english_word_date=user_english_word_date,
                form=search_form,
                delete_form=delete_form,
                back_form=back_form,
                user=username.username,
                user_status=user_status
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
                back_form=back_form,
                translation_form=translation_form,
                user=username.username,
                user_status=user_status
                )
        return redirect(url_for('.user_engdict_index', username=username.username))


@blueprint.route('/user-process-engdict-insert/<username>', methods=['POST'])
def user_process_engdict_insert(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Ваш английский словарь'
    search_form = EngDictionarySearchForm()
    form = WordInsertForm()
    word_in_form = form.insert.data
    word = session.get('word')
    english_word, translation = user_engdict_add_word(word_in_form, word, username)
    back_form = BackToEngDictionary()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_engdict_insert_completed.html',
        page_title=title,
        english_word=english_word,
        translation=translation,
        form=search_form,
        back_form=back_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user-delete-engword/<username>', methods=['POST'])
def user_delete_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    word = session.get('word')
    deleted_word = user_engdict_delete_word(word, username)
    flash(f'Слово {deleted_word.word_itself} удалено из вашего английского словаря')
    return redirect(url_for('.user_engdict_index', username=username.username))


@blueprint.route('/user-engdict-back/<username>', methods=['POST'])
def user_engdict_back(username):
    username = User.query.filter_by(username=username).first_or_404()
    return redirect(url_for('.user_engdict_index', username=username.username))


@blueprint.route('/user_frenchdict/<username>')
def user_frenchdict_index(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = 'Ваш французский словарь'
    french_list = process_user_frenchdict_index(username)
    french_words_sum = len(french_list)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_frenchdict_index.html',
        page_title=title,
        french_list=french_list,
        french_list_len=french_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_frenchdict_new/<username>')
def user_frenchdict_index_new(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = 'Ваш французский словарь'
    french_list = process_user_frenchdict_index(username)
    french_list_new = [word for word in french_list if word[1] == 'new']
    french_words_sum = len(french_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_frenchdict_index_new.html',
        page_title=title,
        french_list=french_list_new,
        french_list_len=french_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_frenchdict_familiar/<username>')
def user_frenchdict_index_familiar(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = 'Ваш французский словарь'
    french_list = process_user_frenchdict_index(username)
    french_list_new = [word for word in french_list if word[1] == 'familiar']
    french_words_sum = len(french_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_frenchdict_index_familiar.html',
        page_title=title,
        french_list=french_list_new,
        french_list_len=french_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user_frenchdict_forgotten/<username>')
def user_frenchdict_index_forgotten(username):
    username = User.query.filter_by(username=username).first_or_404()
    search_form = FrenchDictionarySearchForm()
    title = 'Ваш французский словарь'
    french_list = process_user_frenchdict_index(username)
    french_list_new = [word for word in french_list if word[1] == 'forgotten']
    french_words_sum = len(french_list_new)
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_frenchdict_index_forgotten.html',
        page_title=title,
        french_list=french_list_new,
        french_list_len=french_words_sum,
        form=search_form,
        user=username.username,
        user_status=user_status
        )


@blueprint.route('/user-process-frenchdict-search/<username>', methods=['POST'])
def user_process_frenchdict_search(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Ваш французский словарь'
    search_form = FrenchDictionarySearchForm()
    delete_form = DeleteFrenchWordButton()
    back_form = BackToFrenchDictionary()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    if search_form.validate_on_submit():
        word_in_form, word = search_form.word.data, None
        session['word'] = search_form.word.data
        word, user_french_word_status, user_french_word_date, userword_id = user_frenchdict_search(
            word_in_form,
            username
            )

        if word:
            return render_template(
                'dictionary/user_frenchdict_search.html',
                page_title=title,
                french_word=word,
                french_word_status=user_french_word_status,
                french_word_date=user_french_word_date,
                form=search_form,
                delete_form=delete_form,
                back_form=back_form,
                user=username.username,
                user_status=user_status
                )

        flash('Такого слова нет в вашем французском словаре')
        translation = user_frenchdict_translate(word_in_form)
        if translation:
            translation_form = WordInsertForm()
            return render_template(
                'dictionary/user_frenchdict_insert.html',
                page_title=title,
                french_word=word_in_form,
                translation=translation,
                form=search_form,
                back_form=back_form,
                translation_form=translation_form,
                user=username.username,
                user_status=user_status
                )
        return redirect(url_for('.user_frenchdict_index', username=username.username))


@blueprint.route('/user-process-frenchdict-insert/<username>', methods=['POST'])
def user_process_frenchdict_insert(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Ваш французский словарь'
    search_form = FrenchDictionarySearchForm()
    form = WordInsertForm()
    back_form = BackToFrenchDictionary()
    word_in_form = form.insert.data
    word = session.get('word')
    french_word, translation = user_frenchdict_add_word(word_in_form, word, username)
    back_form = BackToFrenchDictionary()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template(
        'dictionary/user_frenchdict_insert_completed.html',
        page_title=title,
        french_word=french_word,
        translation=translation,
        form=search_form,
        back_form=back_form,
        user_status=user_status
        )


@blueprint.route('/user-delete-frenchword/<username>', methods=['POST'])
def user_delete_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    word = session.get('word')
    deleted_word = user_frenchdict_delete_word(word, username)
    flash(f'Слово {deleted_word.word_itself} удалено из вашего французского словаря')
    return redirect(url_for('.user_frenchdict_index', username=username.username))


@blueprint.route('/user-frenchdict-back/<username>', methods=['POST'])
def user_frenchdict_back(username):
    username = User.query.filter_by(username=username).first_or_404()
    return redirect(url_for('.user_frenchdict_index', username=username.username))
