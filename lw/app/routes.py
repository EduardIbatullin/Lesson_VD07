from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from lw.app.models import User
from lw.app import db, app, bcrypt
from lw.app.forms import LoginForm, RegistrationForm


# Декоратор для перенаправления на главную страницу
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


# Декоратор для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались. Можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Декоратор для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Неправильный логин или пароль. Пожалуйста, попробуйте ещё раз.', 'danger')
    return render_template('login.html', title='Login', form=form)


# Декоратор для выхода
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Декоратор для страницы профиля
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
