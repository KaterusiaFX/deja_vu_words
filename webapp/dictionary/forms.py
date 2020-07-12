from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EngDictionarySearchForm(FlaskForm):
    word = StringField(
        'Поиск по английскому словарю',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
        )
    search = SubmitField('Поиск', render_kw={"class": "btn btn-info"})


class FrenchDictionarySearchForm(FlaskForm):
    word = StringField(
        'Поиск по французскому словарю',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
        )
    search = SubmitField('Поиск', render_kw={"class": "btn btn-info"})


class DeleteEngWordButton(FlaskForm):
    delete = SubmitField('Удалить слово', render_kw={"class": "btn btn-outline-danger"})


class DeleteFrenchWordButton(FlaskForm):
    delete = SubmitField('Удалить слово', render_kw={"class": "btn btn-outline-danger"})


class WordInsertForm(FlaskForm):
    insert = StringField(
        'Ввести собственный вариант перевода:',
        render_kw={"class": "form-control"}
        )
    add = SubmitField('Добавить слово', render_kw={"class": "btn btn-outline-success"})
