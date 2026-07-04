from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Score, Topic
from __init__ import db
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    # Menghitung statistik kuis per topik
    stats_query = db.session.query(
        Topic.id,
        Topic.name, 
        func.count(Score.id).label('total_kuis')
    ).outerjoin(Score, (Topic.id == Score.topic_id) & (Score.user_id == current_user.id))\
    .group_by(Topic.name).all()
    
    stats_kuis = {name: total for _, name, total in stats_query}
    topik_kuis = {name: id for id, name, _ in stats_query}

    last_attempts = {}

    for slug, t_id in topik_kuis.items():
        quiz_attempt = Score.query.filter_by(user_id=current_user.id, topic_id=t_id)\
                             .order_by(Score.date_posted.desc())\
                             .first()
        if quiz_attempt:
            last_attempts[slug] = quiz_attempt.date_posted.strftime('%d %B %Y - %H:%M')
        else:
            last_attempts[slug] = 'Belum Pernah'

    riwayat_deteksi = current_user.deteksi
    total_deteksi = len(riwayat_deteksi)
    
    return render_template('profile.html', 
                           stats_kuis=stats_kuis, 
                           total_deteksi=total_deteksi, 
                           riwayat_deteksi=riwayat_deteksi,
                           last_attempts=last_attempts
                           )