from flask import Blueprint, render_template
from random import choice, random, sample

from webapp.dictionary.dict_functions import process_user_engdict_index, process_user_frenchdict_index
from webapp.dictionary.dict_functions import user_engdict_search, user_frenchdict_search
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
    other_words = [word for word in new_words if word != guess_word]
    other_words = sample(other_words, 4)
    other_words.append(guess_word)
    mixture = sorted(other_words, key=lambda x: random())
    return render_template('exercises/word_translation.html', guess_word=guess_word, mixture=mixture)


@blueprint.route('/engword_translation_answer/<username>')
def engword_translation_answer(username, guess_word, user_answer, mixture):
    username = User.query.filter_by(username=username).first_or_404()
    pic = 'right.jpg'
    return render_template('exercises/word_translation.html', guess_word=guess_word, mixture=mixture, pic=pic)
