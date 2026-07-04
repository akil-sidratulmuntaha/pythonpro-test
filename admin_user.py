import os
from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from __init__ import db
from models import User

# Inisialisasi Blueprint khusus Manajemen User Admin
admin_user = Blueprint('admin_user', __name__)

@admin_user.route('/admin/users')
@login_required
def admin_users():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    all_users = User.query.order_by(User.id.desc()).all()
    return render_template('admin_users.html', users=all_users)

@admin_user.route('/admin/users/add', methods=['POST'])
@login_required
def add_user():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    is_admin = True if request.form.get('is_admin') == 'on' else False

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        flash('Email sudah terdaftar!', 'danger')
        return redirect(url_for('admin_user.admin_users'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='scrypt'),
        is_admin=is_admin
    )
    
    db.session.add(new_user)
    db.session.commit()
    flash('Pengguna baru berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_user.admin_users'))

@admin_user.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        if user.id != current_user.id:
            user.is_admin = True if request.form.get('is_admin') == 'on' else False
            ada_peringatan = False
        else:
            # Jika mengedit diri sendiri, paksa tetap True agar tidak kehilangan akses
            if request.form.get('is_admin') != 'on':
                flash('Tidak bisa menghilangkan akses diri sendiri sebagai admin!', 'error')
                ada_peringatan = True
            user.is_admin = True
        
        new_password = request.form.get('password')
        if new_password:
            user.password = generate_password_hash(new_password, method='scrypt')
            
        db.session.commit()

        if not ada_peringatan:
            flash('Data pengguna berhasil diperbarui!', 'success')
        return redirect(url_for('admin_user.admin_users'))
        
    return render_template('edit_users.html', user=user)

@admin_user.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('Anda tidak dapat menghapus akun Anda sendiri yang sedang digunakan!', 'danger')
        return redirect(url_for('admin_user.admin_users'))
        
    db.session.delete(user)
    db.session.commit()
    flash('Pengguna berhasil dihapus!', 'success')
    return redirect(url_for('admin_user.admin_users'))