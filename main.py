import os, cv2, random
from flask import Blueprint, render_template, url_for, request, redirect, session, current_app, abort
from flask_login import login_required, current_user
from .models import User, Question, Score, DetectionHistory
from . import db
from werkzeug.utils import secure_filename
from imageai.Detection import ObjectDetection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    #Statistic current user mengambil kuis per topik
    stats_kuis = {
        'bot_discord': Score.query.filter_by(user_id=current_user.id, topic='bot_discord').count(),
        'ai_vision': Score.query.filter_by(user_id=current_user.id, topic='ai_vision').count(),
        'flask': Score.query.filter_by(user_id=current_user.id, topic='flask').count(),
        'nlp': Score.query.filter_by(user_id=current_user.id, topic='nlp').count(),
    }
    
    #Statistic deteksi objek yang pernah dilakukan current user
    total_deteksi = DetectionHistory.query.filter_by(user_id=current_user.id).count()
    
    #History file hasil deteksi yang hanya dilakukan current user
    riwayat_deteksi = DetectionHistory.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', 
                           stats_kuis=stats_kuis, 
                           total_deteksi=total_deteksi, 
                           riwayat_deteksi=riwayat_deteksi,
                           name=current_user.name)    

@main.route('/admin')
@login_required
def admin_dashboard():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    total_users = User.query.count()
    total_questions = Question.query.count()
    total_detections = DetectionHistory.query.count()
    
    return render_template('admin_dash.html', 
                           total_users=total_users, 
                           total_questions=total_questions,
                           total_detections=total_detections)

@main.route('/admin/questions')
@login_required
def admin_questions():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    #Ambil dan tampilkan semua pertanyaan di dashboard admin
    all_questions = Question.query.order_by(Question.topic).all()
    return render_template('admin_question.html', questions=all_questions)

@main.route('/admin/questions/add', methods=['POST'])
@login_required
def add_question():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    topic = request.form.get('topic')
    text = request.form.get('text')
    option_a = request.form.get('option_a')
    option_b = request.form.get('option_b')
    option_c = request.form.get('option_c')
    correct_answer = request.form.get('correct_answer')

    new_q = Question(
        topic=topic,
        text=text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        correct_answer=correct_answer
    )
    db.session.add(new_q)
    db.session.commit()
    return redirect(url_for('main.admin_questions'))


@main.route('/admin/questions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    question = Question.query.get_or_404(id)
    
    if request.method == 'POST':
        question.topic = request.form.get('topic')
        question.text = request.form.get('text')
        question.option_a = request.form.get('option_a')
        question.option_b = request.form.get('option_b')
        question.option_c = request.form.get('option_c')
        question.correct_answer = request.form.get('correct_answer')
        
        db.session.commit()
        return redirect(url_for('main.admin_questions'))
        
    return render_template('edit_question.html', question=question)


@main.route('/admin/questions/delete/<int:id>', methods=['POST'])
@login_required
def delete_question(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
        
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('main.admin_questions'))

@main.route('/quiz')
@login_required
def quiz():
    count = 0
    
    selected_topic = request.args.get('topic')

    selected_questions = Question.query.filter_by(topic=selected_topic).all()

    for questions in selected_questions:
        count += 1 

    global_high_score = db.session.query(db.func.max(Score.score)).filter(Score.topic==selected_topic).scalar() or 0
    user_high_score = db.session.query(db.func.max(Score.score)).filter(Score.user_id == current_user.id, Score.topic==selected_topic).scalar() or 0

    return render_template('quiz.html', topic=selected_topic, questions=selected_questions, global_high_score=global_high_score, user_high_score=user_high_score, name=current_user.name, count = count)

@main.route('/submit', methods=['POST'])
@login_required
def submit():
    score = 0
    count = 0 

    #Ambil topik langsung dari form input hidden yang dikirim
    selected_topic = request.form.get('topic')
    
    if not selected_topic:
        return "Topik tidak ditemukan", 400

    questions = Question.query.filter_by(topic=selected_topic).all()
    

    for question in questions:
        user_answer = request.form.get(f"q{question.id}")
        if user_answer == question.correct_answer:
            score += 1
        count += 1
    

    new_score = Score(user_id=current_user.id, topic=selected_topic, score=score)
    db.session.add(new_score)
    db.session.commit()

    global_high_score = db.session.query(db.func.max(Score.score)).filter(Score.topic==selected_topic).scalar()
    user_high_score = db.session.query(db.func.max(Score.score)).filter(Score.user_id == current_user.id, Score.topic==selected_topic).scalar()

    return render_template('result.html', topic=selected_topic, score=score, global_high_score=global_high_score, user_high_score=user_high_score, user_name=current_user.name, count = count)

@main.route('/reset', methods=['POST'])
@login_required
def reset_highest_score():
    topic_to_del = request.form.get('topic')

    db.session.query(Score).filter(Score.topic == topic_to_del).delete()
    db.session.commit()
    return redirect(url_for('main.quiz', topic=topic_to_del))

@main.route('/deteksi_ai', methods=['GET','POST'])
@login_required
def deteksi_ai():
    # Proses Deteksi Objek Menggunakan Tiny YoloV3
    detector = ObjectDetection()
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(BASE_DIR, 'models', 'tiny-yolov3.pt')

    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    #Memanggil Upload Folder untuk deteksi objek pada gambar di current_app (__init__.py):
    folder_upload = current_app.config['UPLOAD_FOLDER']
    folder_output = current_app.config['OUTPUT_FOLDER']
    
    input_web_path = None
    output_web_path = None
    results = []

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(folder_upload, filename)
            output_path = os.path.join(folder_output, 'result_' + filename)
            file.save(input_path)

            #Menjalankan Deteksi Objek
            detections = detector.detectObjectsFromImage(
                input_image=input_path, 
                output_image_path=None
            )

            image = cv2.imread(input_path)
            # warna_kelas = {}
            nomor_objek = 0

            #Menyimpan hasil deteksi objek pada gambar ke dictionary results dan web
            for item in detections:
                nama_objek = item["name"]
                nomor_objek += 1
                results.append({
                    'nomor': nomor_objek,
                    'name': item["name"],
                    'probability': round(item["percentage_probability"], 2)
                })
                
                # if nama_objek not in warna_kelas:
                #     B = random.randint(0, 255)
                #     G = random.randint(0, 255)
                #     R = random.randint(0, 255)
                #     warna_kelas[nama_objek] = (B, G, R)
                
                # 3. Ambil warna yang sesuai untuk objek ini
                warna_bgr = (0, 255, 255)
                
                box = item["box_points"]
                x1, y1, x2, y2 = box[0], box[1], box[2], box[3]

                cv2.rectangle(image, (x1, y1), (x2, y2), warna_bgr, 2)
                # Gambar teks kuning di atas kotak
                # Menggunakan font standard OpenCV, ukuran 0.6, ketebalan 2
                #label = f"{item['name']}: {round(item['percentage_probability'], 1)}%"
                cv2.putText(image, str(nomor_objek), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, warna_bgr, 2)

            #Menyimpan gambar hasil kustomisasi OpenCV ke folder output
            cv2.imwrite(output_path, image)

            #Menyimpan file hasil deteksi objek ke db
            new_detection = DetectionHistory(
                filename='result_' + filename,
                user_id=current_user.id
            )
            db.session.add(new_detection)
            
            db.session.commit()

            input_web_path = f"uploads/{filename}"
            output_web_path = f"output/result_{filename}"

    return render_template('ai.html', 
                           input_image=input_web_path, 
                           output_image=output_web_path, 
                           results=results)