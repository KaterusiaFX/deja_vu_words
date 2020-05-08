import re

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from random import choice, random, sample

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.exercises.forms import InsertWordForm
from webapp.exercises.exercise_functions import engword_translation_training, frenchword_translation_training
from webapp.exercises.exercise_functions import insert_engword_training, insert_frenchword_training
from webapp.exercises.exercise_functions import insert_translation_of_engword_training
from webapp.exercises.exercise_functions import insert_translation_of_frenchword_training
from webapp.exercises.exercise_functions import not_remember_engword_training, not_remember_frenchword_training
from webapp.exercises.exercise_functions import remember_engword_training, remember_frenchword_training
from webapp.exercises.exercise_functions import translation_engword_training, translation_frenchword_training
from webapp.user.models import User
from webapp.user.views import check_teacher_student

blueprint = Blueprint('exercises', __name__, url_prefix='/exercises')


@blueprint.route('/choose_exercise/<username>')
def choose_exercise(username):
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template('exercises/choose_exercise.html', user_status=user_status)


@blueprint.route('/engword_translation/<username>')
def engword_translation(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[5] is not None, process_user_engdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        new_words_for_other_words_sampling = list(filter(
            lambda x: x[1] == 'new',
            process_user_engdict_index(username)
            ))
        guess_word = choice(new_words)
        other_words = [word[0].translation_rus for word in new_words_for_other_words_sampling if word != guess_word]
        other_words = sample(other_words, 4)
        other_words.append(guess_word[0].translation_rus)
        mixture = sorted(other_words, key=lambda x: random())
        return render_template(
            'exercises/engword_translation.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            mixture=mixture,
            user_status=user_status
            )
    return render_template('exercises/engword_translation.html', user_status=user_status)


@blueprint.route('/engword_translation_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def engword_translation_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    mixture = mixture.split(', ')
    mixture = [re.findall('[а-яА-Я-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = engword_translation_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/engword_translation_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision,
        user_status=user_status
        )


@blueprint.route('/translation_engword/<username>')
def translation_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[6] is not None, process_user_engdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        new_words_for_other_words_sampling = list(filter(
            lambda x: x[1] == 'new',
            process_user_engdict_index(username)
            ))
        guess_word = choice(new_words)
        other_words = [word[0].word_itself for word in new_words_for_other_words_sampling if word != guess_word]
        other_words = sample(other_words, 4)
        other_words.append(guess_word[0].word_itself)
        mixture = sorted(other_words, key=lambda x: random())
        return render_template(
            'exercises/translation_engword.html',
            guess_word=guess_word[0].translation_rus,
            new_words_number=new_words_number,
            mixture=mixture,
            user_status=user_status
            )
    return render_template('exercises/translation_engword.html', user_status=user_status)


@blueprint.route('/translation_engword_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def translation_engword_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    mixture = mixture.split(', ')
    mixture = [re.findall('[a-zA-Z-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = translation_engword_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/translation_engword_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision,
        user_status=user_status
        )


@blueprint.route('/insert_engword/<username>')
def insert_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[7] is not None, process_user_engdict_index(username)))
    new_words_number = len(new_words)
    form = InsertWordForm()
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/insert_engword.html',
            guess_word=guess_word[0].translation_rus,
            new_words_number=new_words_number,
            form=form,
            user_status=user_status
            )
    return render_template('exercises/insert_engword.html', user_status=user_status)


@blueprint.route('/insert_engword_answer/<username>/<guess_word>', methods=['POST'])
def insert_engword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    form = InsertWordForm()
    if form.validate_on_submit():
        user_answer = form.word.data
        decision, true_word = insert_engword_training(username, guess_word, user_answer)
        return render_template(
            'exercises/insert_engword_answer.html',
            true_word=true_word,
            decision=decision,
            user_status=user_status
            )


@blueprint.route('/insert_translation_of_engword/<username>')
def insert_translation_of_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[8] is not None, process_user_engdict_index(username)))
    new_words_number = len(new_words)
    form = InsertWordForm()
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/insert_translation_of_engword.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            form=form,
            user_status=user_status
            )
    return render_template('exercises/insert_translation_of_engword.html', user_status=user_status)


@blueprint.route('/insert_translation_of_engword_answer/<username>/<guess_word>', methods=['POST'])
def insert_translation_of_engword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    form = InsertWordForm()
    if form.validate_on_submit():
        user_answer = form.word.data
        decision, true_word = insert_translation_of_engword_training(username, guess_word, user_answer)
        return render_template(
            'exercises/insert_translation_of_engword_answer.html',
            true_word=true_word,
            decision=decision,
            user_status=user_status
            )


@blueprint.route('/remember_engword/<username>')
def remember_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[9] is not None, process_user_engdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/remember_engword.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            user_status=user_status
            )
    return render_template('exercises/remember_engword.html', user_status=user_status)


@blueprint.route('/remember_engword_answer/<username>/<guess_word>')
def remember_engword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    remember_engword_training(username, guess_word)
    return redirect(url_for('.remember_engword', username=username.username))


@blueprint.route('/not_remember_engword_answer/<username>/<guess_word>')
def not_remember_engword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    not_remember_engword_training(username, guess_word)
    return redirect(url_for('.remember_engword', username=username.username))


@blueprint.route('/frenchword_translation/<username>')
def frenchword_translation(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[5] is not None, process_user_frenchdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        new_words_for_other_words_sampling = list(filter(
            lambda x: x[1] == 'new',
            process_user_frenchdict_index(username)
            ))
        guess_word = choice(new_words)
        other_words = [word[0].translation_rus for word in new_words_for_other_words_sampling if word != guess_word]
        other_words = sample(other_words, 4)
        other_words.append(guess_word[0].translation_rus)
        mixture = sorted(other_words, key=lambda x: random())
        return render_template(
            'exercises/frenchword_translation.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            mixture=mixture,
            user_status=user_status
            )
    return render_template('exercises/frenchword_translation.html', user_status=user_status)


@blueprint.route('/frenchword_translation_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def frenchword_translation_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    mixture = mixture.split(', ')
    mixture = [re.findall('[а-яА-Я]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = frenchword_translation_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/frenchword_translation_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision,
        user_status=user_status
        )


@blueprint.route('/translation_frenchword/<username>')
def translation_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[6] is not None, process_user_frenchdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        new_words_for_other_words_sampling = list(filter(
            lambda x: x[1] == 'new',
            process_user_frenchdict_index(username)
            ))
        guess_word = choice(new_words)
        other_words = [word[0].word_itself for word in new_words_for_other_words_sampling if word != guess_word]
        other_words = sample(other_words, 4)
        other_words.append(guess_word[0].word_itself)
        mixture = sorted(other_words, key=lambda x: random())
        return render_template(
            'exercises/translation_frenchword.html',
            guess_word=guess_word[0].translation_rus,
            new_words_number=new_words_number,
            mixture=mixture,
            user_status=user_status
            )
    return render_template('exercises/translation_frenchword.html', user_status=user_status)


@blueprint.route('/translation_frenchword_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def translation_frenchword_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    mixture = mixture.split(', ')
    mixture = [re.findall('[a-zA-Z-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = translation_frenchword_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/translation_frenchword_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision,
        user_status=user_status
        )


@blueprint.route('/insert_frenchword/<username>')
def insert_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[7] is not None, process_user_frenchdict_index(username)))
    new_words_number = len(new_words)
    form = InsertWordForm()
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/insert_frenchword.html',
            guess_word=guess_word[0].translation_rus,
            new_words_number=new_words_number,
            form=form,
            user_status=user_status
            )
    return render_template('exercises/insert_frenchword.html', user_status=user_status)


@blueprint.route('/insert_frenchword_answer/<username>/<guess_word>', methods=['POST'])
def insert_frenchword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    form = InsertWordForm()
    if form.validate_on_submit():
        user_answer = form.word.data
        decision, true_word = insert_frenchword_training(username, guess_word, user_answer)
        return render_template(
            'exercises/insert_frenchword_answer.html',
            true_word=true_word,
            decision=decision,
            user_status=user_status
            )


@blueprint.route('/insert_translation_of_frenchword/<username>')
def insert_translation_of_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[8] is not None, process_user_frenchdict_index(username)))
    new_words_number = len(new_words)
    form = InsertWordForm()
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/insert_translation_of_frenchword.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            form=form,
            user_status=user_status
            )
    return render_template('exercises/insert_translation_of_frenchword.html', user_status=user_status)


@blueprint.route('/insert_translation_of_frenchword_answer/<username>/<guess_word>', methods=['POST'])
def insert_translation_of_frenchword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    form = InsertWordForm()
    if form.validate_on_submit():
        user_answer = form.word.data
        decision, true_word = insert_translation_of_frenchword_training(username, guess_word, user_answer)
        return render_template(
            'exercises/insert_translation_of_frenchword_answer.html',
            true_word=true_word,
            decision=decision,
            user_status=user_status
            )


@blueprint.route('/remember_frenchword/<username>')
def remember_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    new_words = list(filter(lambda x: x[1] == 'new' and x[9] is not None, process_user_frenchdict_index(username)))
    new_words_number = len(new_words)
    if new_words_number:
        guess_word = choice(new_words)
        return render_template(
            'exercises/remember_frenchword.html',
            guess_word=guess_word[0].word_itself,
            new_words_number=new_words_number,
            user_status=user_status
            )
    return render_template('exercises/remember_frenchword.html', user_status=user_status)


@blueprint.route('/remember_frenchword_answer/<username>/<guess_word>')
def remember_frenchword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    remember_frenchword_training(username, guess_word)
    return redirect(url_for('.remember_frenchword', username=username.username))


@blueprint.route('/not_remember_frenchword_answer/<username>/<guess_word>')
def not_remember_frenchword_answer(username, guess_word):
    username = User.query.filter_by(username=username).first_or_404()
    not_remember_frenchword_training(username, guess_word)
    return redirect(url_for('.remember_frenchword', username=username.username))
