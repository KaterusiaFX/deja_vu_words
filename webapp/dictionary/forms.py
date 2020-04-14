from flask_wtf import FlaskForm
from wtforms import FormField, StringField, SubmitField
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


class BackToEngDictionary(FlaskForm):
    back_eng = SubmitField('Назад в английский словарь', render_kw={"class": "btn btn-outline-info"})


class BackToFrenchDictionary(FlaskForm):
    back_french = SubmitField('Назад во французский словарь', render_kw={"class": "btn btn-outline-info"})


class WordInsertForm(FlaskForm):
    insert = StringField(
        'Ввести собственный вариант перевода:',
        render_kw={"class": "form-control"}
        )
    add = SubmitField('Добавить слово', render_kw={"class": "btn btn-outline-success"})
    back_to_eng = FormField(BackToEngDictionary)
    back_to_french = FormField(BackToFrenchDictionary)
