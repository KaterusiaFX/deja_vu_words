from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class InsertWordForm(FlaskForm):
    word = StringField(validators=[DataRequired()], render_kw={"class": "form-control"})
    send = SubmitField('Отправить', render_kw={"class": "btn btn-info"})
