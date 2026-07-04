from flask import Blueprint, request, redirect, url_for, flash, render_template, abort
from flask_login import login_required, current_user
from models import Question, Topic, User, DetectionHistory
from __init__ import db

admin_bp = Blueprint('admin_bp', __name__)

def admin_required():
    if not getattr(current_user, 'is_admin', False):
        abort(403)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    admin_required()
        
    total_users = User.query.count()
    total_questions = Question.query.count()
    total_detections = DetectionHistory.query.count()
    
    return render_template('admin_dash.html', 
                           total_users=total_users, 
                           total_questions=total_questions,
                           total_detections=total_detections)

@admin_bp.route('/admin/questions')
@login_required
def admin_questions():
    admin_required()

    page = request.args.get('page', 1, type=int)
    per_page = 5

    question_pagination = Question.query.order_by(Question.topic_id).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin_question.html', question_pagination=question_pagination)

@admin_bp.route('/admin/questions/add', methods=['POST'])
@login_required
def add_question():
    admin_required()
    topic = request.form.get('topic')
    text = request.form.get('text')
    option_a = request.form.get('option_a')
    option_b = request.form.get('option_b')
    option_c = request.form.get('option_c')
    correct_answer = request.form.get('correct_answer')

    selected_topic = Topic.query.filter_by(name=topic).first()

    new_q = Question(
        topic_id=selected_topic.id,
        text=text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        correct_answer=correct_answer
    )
    db.session.add(new_q)
    db.session.commit()
    flash('Pertanyaan baru berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_bp.admin_questions'))

@admin_bp.route('/admin/questions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    admin_required()
    question = Question.query.get_or_404(id)
    
    if request.method == 'POST':
        topic = request.form.get('topic')
        selected_topic = Topic.query.filter_by(name=topic).first()
        
        question.topic_id = selected_topic.id
        question.text = request.form.get('text')
        question.option_a = request.form.get('option_a')
        question.option_b = request.form.get('option_b')
        question.option_c = request.form.get('option_c')
        question.correct_answer = request.form.get('correct_answer')
        
        db.session.commit()
        flash('Pertanyaan berhasil diperbarui!', 'success')
        return redirect(url_for('admin_bp.admin_questions'))
        
    return render_template('edit_question.html', question=question)

@admin_bp.route('/admin/questions/delete/<int:id>', methods=['POST'])
@login_required
def delete_question(id):
    admin_required()
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin_bp.admin_questions'))