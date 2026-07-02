from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password') 
    
    if not email or not name or not password:
        flash('Semua kolom pendaftaran wajib diisi dengan benar!', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email atau username sudah terdaftar. Silakan gunakan yang lain!', 'danger')
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password = generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()
    flash('Pendaftaran berhasil! Silakan login.', 'success')
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
    return redirect(url_for('main.index'))