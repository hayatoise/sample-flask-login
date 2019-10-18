from typing import Text

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from application.models import User
from application.database import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # フォームの空欄を確認
    if email == '' or password == '':
        flash('メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('auth.login'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('auth.login'))

    # パスワードの長さは 12 文字以上
    if not 12 <= len(password):
        flash('パスワードは 12 文字以上にして下さい')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    # ユーザ情報の有無を確認
    if not user:
        flash('入力されたメールアドレスが正しくありません')
        return redirect(url_for('auth.login'))

    # パスワードのチェック
    if not check_password_hash(user.password, password):
        flash('入力されたパスワードが正しくありません')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET'])
def signup() -> Text:
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post() -> Text:
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # フォームの空欄を確認
    if name == '' or display_name == '' or email == '' or password == '':
        flash('ユーザ名、表示名、メールアドレスまたはパスワードが空欄です')
        return redirect(url_for('auth.signup'))

    # メールアドレスの重複を確認
    user_by_email = User.query.filter_by(email=email).first()
    if user_by_email:
        flash('このメールアドレスは既に使われています')
        return redirect(url_for('auth.signup'))

    # ユーザ名の重複を確認
    user_by_name = User.query.filter_by(name=name).first()
    if user_by_name:
        flash('このユーザ名は既に使われています')
        return redirect(url_for('auth.signup'))

    # ユーザ名は 2 ~ 15 文字以内
    if not 2 <= len(name) <= 15:
        flash('ユーザ名は 2 ~ 15 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # ユーザ名は英数字のみ
    if name.isalnum() is True:
        name = request.form.get('name').lower()
    else:
        flash('ユーザ名は英数字のみにして下さい')

    # 表示名は 50 文字以内
    if not 1 <= len(display_name) <= 50:
        flash('表示名は 50 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # メールアドレスは 6 ~ 254 文字以内
    if not 6 <= len(email) <= 254:
        flash('メールアドレスは 6 ~ 254 文字以内にして下さい')
        return redirect(url_for('auth.signup'))

    # パスワードの長さは 12 文字以上
    if not 12 <= len(password):
        flash('パスワードは 12 文字以上にして下さい')
        return redirect(url_for('auth.signup'))

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(name=name, display_name=display_name, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout() -> Text:
    logout_user()
    return redirect(url_for('main.index'))
