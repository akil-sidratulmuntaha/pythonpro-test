from __init__ import db
from flask_login import UserMixin

#tabel user (lupa menambahkan timestamp agar bisa menampilkan data latest attempt)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    is_admin = db.Column(db.Boolean, default=False)
    
#tabel pertanyaan quiz
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    topic  = db.Column(db.String(100), nullable = False)
    text = db.Column(db.String(255), nullable = False)
    option_a =  db.Column(db.String(255), nullable=False)
    option_b =  db.Column(db.String(255), nullable=False)
    option_c =  db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable = False)

#tabel riwayat skor quiz 
class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    topic  = db.Column(db.String(100), nullable = False)
    score = db.Column(db.Integer)

#tabel riwayat deteksi objek menggunakan TinyYolov3
class DetectionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable = False)

    