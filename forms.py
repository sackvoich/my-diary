from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', 
                           validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Пароль', 
                             validators=[DataRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('Подтверждение пароля', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', 
                           validators=[DataRequired()])
    password = PasswordField('Пароль', 
                             validators=[DataRequired()])
    submit = SubmitField('Войти')


class EntryForm(FlaskForm):
    content = TextAreaField('Запись', validators=[DataRequired()])
    submit = SubmitField('Сохранить запись')