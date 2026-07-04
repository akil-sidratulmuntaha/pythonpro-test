import os, cv2
from flask import Blueprint, request, redirect, current_app, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from imageai.Detection import ObjectDetection
from models import DetectionHistory
from __init__ import db

detection_bp = Blueprint('detection_bp', __name__)

@detection_bp.route('/deteksi_ai', methods=['GET','POST'])
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

            image = cv2.imread(input_path)
            # warna_kelas = {}
            nomor_objek = 0

            #Menjalankan Deteksi Objek
            detections = detector.detectObjectsFromImage(
                input_image=input_path, 
                output_image_path=False
            )

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