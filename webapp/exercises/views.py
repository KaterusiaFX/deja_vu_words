from flask import Blueprint

blueprint = Blueprint('exercises', __name__, url_prefix='/exercises')


@blueprint.route('/choose_exercise/<username>')
def choose_exercise(username):
    # кнопки с выбором видов тренировок на английском и французском
    pass


@blueprint.route('/word_translation/<username>')
def word_translation(username):
    pass
