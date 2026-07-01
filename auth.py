<<<<<<< HEAD
from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from flask import flash

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password') 
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email atau username sudah terdaftar. Silakan gunakan yang lain!', 'danger')
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password = generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login')) 

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods = ['GET', 'POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email atau password Anda salah, silakan coba lagi.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile')) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
=======
from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db
from flask_login import login_user, logout_user, login_required
from flask import flash

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password') 
    
    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password = generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login')) 

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods = ['GET', 'POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email atau password Anda salah, silakan coba lagi.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile')) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
>>>>>>> b73cd00b7e0ae6d1410a1de57b403e897908a1fa
    return redirect(url_for('main.index'))