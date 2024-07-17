from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from werkzeug.utils import secure_filename
import os
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, MessageForm, ImageUploadForm
from app.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required
from app.analysis import ImgAnalysis

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    message_form = MessageForm()
    upload_form = ImageUploadForm()
    # Получаем сообщения текущего пользователя и сообщения от системного пользователя
    system_user = User.query.filter_by(email='system@messenger.com').first()
    if system_user:
        messages = Message.query.filter(
            (Message.user_id == current_user.id) | (Message.user_id == system_user.id)).order_by(
            Message.date_posted.desc()).all()
    else:
        messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.date_posted.desc()).all()
    return render_template('index.html', title='Home', message_form=message_form, upload_form=upload_form,
                           messages=messages)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Авторизация не прошла. Проверте почту и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route("/message", methods=['POST'])
@login_required
def message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(content=form.content.data, author=current_user)
        db.session.add(message)
        db.session.commit()
        flash('Ваше сообщение успешно отправлено!', 'success')

        # Sending automated response from system user
        system_user = User.query.filter_by(email='system@messenger.com').first()
        if system_user:
            response_message = Message(content="Ваше сообщение получено", author=system_user)
            db.session.add(response_message)
            db.session.commit()
    return redirect(url_for('main.index'))


@bp.route("/upload", methods=['POST'])
@login_required
def upload():
    form = ImageUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_message = Message(content=None, image_file=filename, author=current_user)
            db.session.add(image_message)
            db.session.commit()
            flash('Ваше изображение успешно загружено!', 'success')

            # Sending automated response from system user
            system_user = User.query.filter_by(email='system@messenger.com').first()
            if system_user:
                mess = ImgAnalysis(file)()
                response_message = Message(content=mess, author=system_user)
                db.session.add(response_message)
                db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('Неверный тип файла', 'danger')
            return redirect(url_for('main.index'))
    else:
        flash('Файл не выбран', 'danger')
        return redirect(url_for('main.index'))
