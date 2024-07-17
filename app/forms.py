from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже взято. Выберите что-нибудь другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Эта почта уже взята. Выберите что-нибудь другое.')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
class MessageForm(FlaskForm):
    content = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
class ImageUploadForm(FlaskForm):
    file = FileField('Загрузите изображение', validators=[DataRequired()])
    submit = SubmitField('Загрузить')