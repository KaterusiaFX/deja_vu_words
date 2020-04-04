from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.dictionary.models import EnglishWord, FrenchWord


class EngDictionarySearchForm(FlaskForm):
    word = StringField('Поиск по английскому словарю', validators=[DataRequired()], render_kw={"class": "form-control"})
    search = SubmitField('Поиск', render_kw={"class": "btn btn-info"})

    def validate_word(self, word):
        word = EnglishWord.query.filter_by(word_itself=word.data).first()
        if word is None:
            raise ValidationError('No such a word in our English dictionary')


class FrenchDictionarySearchForm(FlaskForm):
    word = StringField('Поиск по французскому словарю', validators=[DataRequired()], render_kw={"class": "form-control"})
    search = SubmitField('Поиск', render_kw={"class": "btn btn-info"})

    def validate_word(self, word):
        word = FrenchWord.query.filter_by(word_itself=word.data).first()
        if word is None:
            raise ValidationError('No such a word in our French dictionary')
