import os, secrets, sys
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Memuat file .env ke dalam sistem environment variabel
load_dotenv()

from db_instance import db

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_quiz.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #login_manager.login_message = "Silakan Login terlebih dahulu agar dapat mengakses halaman ini."

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from main import main as main_bp
    app.register_blueprint(main_bp)

    from admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    from detection_routes import detection_bp
    app.register_blueprint(detection_bp)

    from quiz_routes import quiz_bp
    app.register_blueprint(quiz_bp)

    from auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    
    from admin_user import admin_user as admin_user_bp
    app.register_blueprint(admin_user_bp)

    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    OUTPUT_FOLDER = os.path.join(app.root_path, 'static', 'output')
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


    with app.app_context():
        #db.drop_all()
        db.create_all()
        
        from models import Question
        if Question.query.first() is None:
             print("Database kuis kosong. Memulai proses pengisian data otomatis...")
             from questions import seed_questions
             seed_questions()

    return app
