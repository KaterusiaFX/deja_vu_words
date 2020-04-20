from flask import Blueprint, render_template

blueprint = Blueprint('exercises', __name__, url_prefix='/exercises')


@blueprint.route('/choose_exercise/<username>')
def choose_exercise(username):
    return render_template('exercises/choose_exercise.html')


@blueprint.route('/word_translation/<username>')
def word_translation(username):
    return render_template('exercises/word_translation.html')
