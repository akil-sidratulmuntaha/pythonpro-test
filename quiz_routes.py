from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Topic, Question, Score
from __init__ import db

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/quiz')
@login_required
def quiz():
    selected_topic = request.args.get('topic')
    current_topic = Topic.query.filter_by(name=selected_topic).first()
    selected_questions = Question.query.filter_by(topic_id=current_topic.id).all()
    count = len(selected_questions)

    global_high_score = db.session.query(db.func.max(Score.score)).filter(Score.topic_id==current_topic.id).scalar() or 0
    user_high_score = db.session.query(db.func.max(Score.score)).filter(Score.user_id == current_user.id, Score.topic_id==current_topic.id).scalar() or 0

    return render_template('quiz.html', 
                           topic=selected_topic, 
                           questions=selected_questions, 
                           global_high_score=global_high_score, 
                           user_high_score=user_high_score, 
                           name=current_user.name, 
                           count=count)

@quiz_bp.route('/submit', methods=['POST'])
@login_required
def submit():
    score = 0
    selected_topic_id = request.form.get('topic')

    if not selected_topic_id:
        return "Topik tidak ditemukan", 400

    current_topic = Topic.query.get(selected_topic_id)
    if not current_topic:
        return "Topik tidak valid", 404

    selected_questions = current_topic.quest
    count = len(selected_questions)
    
    for question in selected_questions:
        user_answer = request.form.get(f"q{question.id}")
        if user_answer == question.correct_answer:
            score += 1

    new_score = Score(user_id=current_user.id, topic_id=current_topic.id, score=score)
    db.session.add(new_score)
    db.session.commit()

    global_high_score = db.session.query(db.func.max(Score.score)).filter(Score.topic_id==current_topic.id).scalar()
    user_high_score = db.session.query(db.func.max(Score.score)).filter(Score.user_id == current_user.id, Score.topic_id==current_topic.id).scalar()

    return render_template('result.html', 
                           topic=current_topic.name, 
                           score=score, 
                           global_high_score=global_high_score, 
                           user_high_score=user_high_score, 
                           user_name=current_user.name, 
                           count=count)

@quiz_bp.route('/reset', methods=['POST'])
@login_required
def reset_highest_score():
    topic_to_del = request.form.get('topic')
    current_topic = Topic.query.filter_by(name=topic_to_del).first()

    db.session.query(Score).filter(Score.topic_id == current_topic.id, Score.user_id == current_user.id).delete()
    db.session.commit()
    return redirect(url_for('quiz_bp.quiz', topic=topic_to_del))