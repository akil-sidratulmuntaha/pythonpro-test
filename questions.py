from __init__ import db, create_app
from models import User, Question
from werkzeug.security import generate_password_hash

#daftar pertanyaan quiz (hard data) per topik untuk di-insert ke db agar tidak perlu menginputkan satu per satu saat testing
bot_discord = [
        Question(text="Platform tempat kita harus mendaftarkan bot baru dan mendapatkan token sebelum mulai menulis kode disebut...",
                 topic = "bot_discord",
                 option_a="Discord Developer Portal", 
                 option_b="Discord Token Generator", 
                 option_c="Discord App Labs", 
                 correct_answer="A"),
        
        Question(text="Jika kita ingin membuat bot Discord menggunakan bahasa pemrograman Python, library/modul populer apa yang biasanya di-install?",
                 topic = "bot_discord", 
                 option_a="discord.js", 
                 option_b="discord.py", 
                 option_c="python-bot", 
                 correct_answer="B"),
        
        Question(text="Apa istilah untuk link/tautan yang digunakan untuk memasukkan bot yang kita buat ke dalam server Discord?",
                 topic = "bot_discord", 
                 option_a="Webhook Link", 
                 option_b="Server Link", 
                 option_c="OAuth2 URL / Invite Link", 
                 correct_answer="C"),
        
        Question(text="Apa fungsi utama dari Token pada Bot Discord?",
                 topic = "bot_discord", 
                 option_a="Sebagai kata sandi rahasia (ID unik) agar kode kita bisa terhubung ke bot di server Discord", 
                 option_b="Untuk mengundang teman masuk ke server", 
                 option_c="Alat pembayaran untuk menyewa server hosting", 
                 correct_answer="A"),
        
        Question(text="Event (kejadian) apa yang dipicu pertama kali saat bot berhasil menyala dan sukses terhubung ke server Discord?",
                 topic = "bot_discord", 
                 option_a="on_start", 
                 option_b="on_connect", 
                 option_c="on_ready", 
                 correct_answer="C"),
    ]

ai_vision = [
        Question(text="Dalam pemrosesan gambar, proses mengubah gambar berwarna menjadi hitam-putih-abu-abu disebut dengan...",
                 topic = "ai_vision",
                 option_a="Resizing", 
                 option_b="Grayscale", 
                 option_c="Normalization", 
                 correct_answer="B"),
        
        Question(text="Mengapa kita sering kali perlu mengubah nilai piksel gambar dari rentang (0 - 255) menjadi rentang (0 - 1) sebelum dimasukkan ke dalam model TensorFlow?",
                 topic = "ai_vision", 
                 option_a="Agar gambar berubah warna menjadi lebih kontras", 
                 option_b="Untuk memperkecil ukuran resolusi gambar", 
                 option_c="Mempercepat proses konvergensi saat pelatihan model (Normalisasi)", 
                 correct_answer="C"),
        
        Question(text="Jika sebuah gambar memiliki resolusi 150 x 150 piksel dan berbasis RGB, bentuk (shape) tensor yang merepresentasikan gambar tersebut adalah...",
                 topic = "ai_vision", 
                 option_a="(150,150)", 
                 option_b="(150,150,1)", 
                 option_c="(150,150,3)", 
                 correct_answer="C"),
        
        Question(text="Komponen dalam TensorFlow yang bertugas memperbarui bobot (weight) model berdasarkan nilai loss saat proses training berlangsung disebut...",
                 topic = "ai_vision", 
                 option_a="Activator", 
                 option_b="Optimizer", 
                 option_c="Evaluator", 
                 correct_answer="B"),
        
        Question(text="Manakah kelas (class) dari pustaka ImageAI yang digunakan jika tugas Anda adalah memprediksi seluruh isi gambar (menentukan satu label objek dominan)?",
                 topic = "ai_vision", 
                 option_a="ImageClassification", 
                 option_b="ObjectDetection", 
                 option_c="VideoObjectDetection", 
                 correct_answer="A"),
    ]

flask = [
        Question(text="Manakah perintah di terminal yang paling tepat untuk menjalankan aplikasi Flask (berkas utama bernama app.py) dalam mode pengembangan (development)",
                 topic = "flask",
                 option_a="python app.py run", 
                 option_b="flask run", 
                 option_c="flask start", 
                 correct_answer="B"),
        
        Question(text="Secara default, server bawaan Flask akan berjalan dan standby menerima request pada port berapa?",
                 topic = "flask", 
                 option_a="3000", 
                 option_b="8000", 
                 option_c="5000", 
                 correct_answer="C"),
        
        Question(text="Method HTTP bawaan yang diizinkan oleh Flask secara default jika kita tidak menentukannya secara eksplisit pada argumen methods adalah...",
                 topic = "flask", 
                 option_a="GET", 
                 option_b="POST", 
                 option_c="PUT", 
                 correct_answer="A"),
        
        Question(text="Fungsi bawaan Flask yang digunakan untuk mengalihkan pengguna secara otomatis dari satu halaman ke halaman lain adalah...",
                 topic = "flask", 
                 option_a="redirect()", 
                 option_b="url_for()", 
                 option_c="render_template()", 
                 correct_answer="A"),
        
        Question(text="Pustaka/engine bawaan Flask yang bertugas merender file HTML dan menyisipkan variabel dari Python ke HTML bernama...",
                 topic = "flask", 
                 option_a="Blade", 
                 option_b="Jinja2", 
                 option_c="Mako", 
                 correct_answer="B"),
    ]

nlp = [
        Question(text="Library Python yang paling populer digunakan untuk mengambil, mengurai (parsing), dan mengekstrak data dari dokumen HTML atau XML adalah...",
                 topic = "nlp",
                 option_a="Numpy", 
                 option_b="BeautifulSoup", 
                 option_c="Scikit-Learn", 
                 correct_answer="B"),
        
        Question(text="Proses memecah sebaris teks atau paragraf menjadi potongan-potongan kecil seperti kata atau kalimat disebut dengan...",
                 topic = "nlp", 
                 option_a="Stemming", 
                 option_b="Tokenization", 
                 option_c="Parsing", 
                 correct_answer="B"),
        
        Question(text="Proses mengubah semua huruf di dalam teks menjadi huruf kecil (lowercase) semua agar seragam disebut...",
                 topic = "nlp", 
                 option_a="Tokenizing", 
                 option_b="Lemmatizing", 
                 option_c="Case Folding", 
                 correct_answer="C"),
        
        Question(text="Apa yang dimaksud dengan Stopwords dalam konteks pemrosesan bahasa alami?",
                 topic = "nlp", 
                 option_a="Kata-kata mutiara yang penting untuk disimpan", 
                 option_b="Kata-kata umum yang sering muncul namun tidak memiliki makna penting", 
                 option_c="Kata-kata kasar yang harus disensor oleh sistem karena tidak pantas", 
                 correct_answer="B"),
        
        Question(text="Jika kata studies diproses menggunakan Porter Stemmer, hasilnya kemungkinan adalah \"studi\". Namun jika diproses menggunakan Lemmatizer (WordNet), kata dasar yang dihasilkan secara akurat sesuai kamus adalah...",
                 topic = "nlp", 
                 option_a="Study", 
                 option_b="Stud", 
                 option_c="Studying", 
                 correct_answer="A"),
    ]
def seed_questions():
    db.session.add_all(bot_discord)
    db.session.add_all(ai_vision)
    db.session.add_all(flask)
    db.session.add_all(nlp)
    db.session.commit()
    print("Data kuis bot_discord, ai_vision, flask, dan NLP berhasil dimasukkan!")

    admin_exists = User.query.filter_by(name='admin').first()
    if not admin_exists:
        admin_user = User(email='admin@gmail.com',
                          name='admin',
                          password=generate_password_hash('admin123'),
                          is_admin=True
                         )
        db.session.add(admin_user)