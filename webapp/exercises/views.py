from flask import Blueprint, render_template
from random import choice, random, sample
import re

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.user.models import User

blueprint = Blueprint('exercises', __name__, url_prefix='/exercises')


@blueprint.route('/choose_exercise/<username>')
def choose_exercise(username):
    return render_template('exercises/choose_exercise.html')


@blueprint.route('/engword_translation/<username>')
def engword_translation(username):
    username = User.query.filter_by(username=username).first_or_404()
    new_words = list(filter(lambda  x: x[1] == 'new', process_user_engdict_index(username)))
    guess_word = choice(new_words)
    other_words = [word[0].translation_rus for word in new_words if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word[0].translation_rus)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template('exercises/word_translation.html', guess_word=guess_word[0].word_itself, mixture=mixture)


# убрать кнопку "Показать варианты", чтобы они были сразу развернуты
@blueprint.route('/engword_translation_answer/<username>/<user_answer>/<guess_word>/<mixture>')
def engword_translation_answer(username, user_answer, guess_word, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    mixture = mixture.split(', ')
    mixture = [re.findall('[а-яА-Я]+', x) for x in mixture]
    new_mixture = [mixture[0][0], mixture[1][0], mixture[2][0], mixture[3][0], mixture[4][0]]
    return render_template('exercises/word_translation.html', guess_word=guess_word, mixture=new_mixture)
