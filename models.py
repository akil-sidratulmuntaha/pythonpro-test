from __init__ import db
from flask_login import UserMixin
from datetime import datetime, timedelta, timezone

def waktu_wib():
    # UTC + 7 jam = WIB
    return datetime.now(timezone(timedelta(hours=7)))

#tabel user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship antara Tabel User-Score
    scores = db.relationship('Score', backref='peserta', cascade="all, delete-orphan", lazy=True)
    # Relationship antara Tabel User-DetectionHistory
    deteksi = db.relationship('DetectionHistory', backref='pemilik', cascade="all, delete-orphan", lazy=True)

#tabel topic
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship antara Tabel Topic-Question
    quest = db.relationship('Question', backref='topic_question_rel', cascade="all, delete-orphan", lazy=True)
    # Relationship antara Tabel Topic-Score
    scores = db.relationship('Score', backref='topik_score_rel', cascade="all, delete-orphan", lazy=True)
    
#tabel pertanyaan quiz
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(255), nullable = False)
    option_a =  db.Column(db.String(255), nullable=False)
    option_b =  db.Column(db.String(255), nullable=False)
    option_c =  db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable = False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

#tabel riwayat skor quiz
class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, nullable = False, default = waktu_wib)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False) 

#tabel riwayat deteksi objek menggunakan TinyYolov3
class DetectionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable = False, default = waktu_wib)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    