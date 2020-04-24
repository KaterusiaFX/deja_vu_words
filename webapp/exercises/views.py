from flask import Blueprint, render_template
from random import choice, random, sample
import re

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.exercises.exercise_functions import engword_translation_training, frenchword_translation_training
from webapp.exercises.exercise_functions import translation_engword_training, translation_frenchword_training
from webapp.user.models import User

blueprint = Blueprint('exercises', __name__, url_prefix='/exercises')


@blueprint.route('/choose_exercise/<username>')
def choose_exercise(username):
    return render_template('exercises/choose_exercise.html')


@blueprint.route('/engword_translation/<username>')
def engword_translation(username):
    username = User.query.filter_by(username=username).first_or_404()
    new_words = list(filter(lambda x: x[1] == 'new' and x[5] != None, process_user_engdict_index(username)))
    new_words_for_other_words_sampling = list(filter(lambda x: x[1] == 'new', process_user_engdict_index(username)))
    guess_word = choice(new_words)
    other_words = [word[0].translation_rus for word in new_words_for_other_words_sampling if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word[0].translation_rus)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template(
        'exercises/engword_translation.html',
        guess_word=guess_word[0].word_itself,
        mixture=mixture
        )


@blueprint.route('/engword_translation_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def engword_translation_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    mixture = mixture.split(', ')
    mixture = [re.findall('[а-яА-Я-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = engword_translation_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/engword_translation_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision
        )


@blueprint.route('/translation_engword/<username>')
def translation_engword(username):
    username = User.query.filter_by(username=username).first_or_404()
    new_words = list(filter(lambda x: x[1] == 'new' and x[6] != None, process_user_engdict_index(username)))
    new_words_for_other_words_sampling = list(filter(lambda x: x[1] == 'new', process_user_engdict_index(username)))
    guess_word = choice(new_words)
    other_words = [word[0].word_itself for word in new_words_for_other_words_sampling if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word[0].word_itself)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template(
        'exercises/translation_engword.html',
        guess_word=guess_word[0].translation_rus,
        mixture=mixture
        )
    

@blueprint.route('/translation_engword_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def translation_engword_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    mixture = mixture.split(', ')
    mixture = [re.findall('[a-zA-Z-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = translation_engword_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/translation_engword_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision
        )


@blueprint.route('/frenchword_translation/<username>')
def frenchword_translation(username):
    username = User.query.filter_by(username=username).first_or_404()
    new_words = list(filter(lambda x: x[1] == 'new' and x[5] != None, process_user_frenchdict_index(username)))
    new_words_for_other_words_sampling = list(filter(lambda x: x[1] == 'new', process_user_frenchdict_index(username)))
    guess_word = choice(new_words)
    other_words = [word[0].translation_rus for word in new_words_for_other_words_sampling if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word[0].translation_rus)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template(
        'exercises/frenchword_translation.html',
        guess_word=guess_word[0].word_itself,
        mixture=mixture
        )


@blueprint.route('/frenchword_translation_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def frenchword_translation_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    mixture = mixture.split(', ')
    mixture = [re.findall('[а-яА-Я]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = frenchword_translation_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/frenchword_translation_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision
        )


@blueprint.route('/translation_frenchword/<username>')
def translation_frenchword(username):
    username = User.query.filter_by(username=username).first_or_404()
    new_words = list(filter(lambda x: x[1] == 'new' and x[6] != None, process_user_frenchdict_index(username)))
    new_words_for_other_words_sampling = list(filter(lambda x: x[1] == 'new', process_user_frenchdict_index(username)))
    guess_word = choice(new_words)
    other_words = [word[0].word_itself for word in new_words_for_other_words_sampling if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word[0].word_itself)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template(
        'exercises/translation_frenchword.html',
        guess_word=guess_word[0].translation_rus,
        mixture=mixture
        )
    

@blueprint.route('/translation_frenchword_answer/<username>/<int:user_answer>/<guess_word>/<mixture>')
def translation_frenchword_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    mixture = mixture.split(', ')
    mixture = [re.findall('[a-zA-Z-]+', x) for x in mixture]
    final_mixture = [' '.join(word) if len(word) > 1 else word[0] for word in mixture]
    decision, true_word = translation_frenchword_training(username, guess_word, final_mixture[user_answer])
    return render_template(
        'exercises/translation_frenchword_answer.html',
        true_word=true_word,
        mixture=final_mixture,
        decision=decision
        )
