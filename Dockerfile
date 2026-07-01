<<<<<<< HEAD
# 1. Gunakan image Python resmi versi ringan
FROM python:3.10-slim

# 2. Atur direktori kerja di dalam server cloud
WORKDIR /code

# 3. Instal dependensi sistem operasi yang dibutuhkan oleh OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Salin berkas requirements.txt terlebih dahulu
COPY ./requirements.txt /code/requirements.txt

# 5. Instal seluruh library Python dengan optimasi tanpa cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 6. Salin seluruh sisa berkas proyek (termasuk folder templates, static, models, dll.)
COPY . .

# 7. Berikan hak akses penuh ke folder proyek agar Flask bisa menulis database SQLite dan menyimpan gambar hasil deteksi
RUN chmod -R 777 /code

# 8. Perintah utama untuk menyalakan aplikasi kuis Anda
CMD ["python", "app.py"]
=======
# 1. Gunakan image Python resmi versi ringan
FROM python:3.10-slim

# 2. Atur direktori kerja di dalam server cloud
WORKDIR /code

# 3. Instal dependensi sistem operasi yang dibutuhkan oleh OpenCV
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Salin berkas requirements.txt terlebih dahulu
COPY ./requirements.txt /code/requirements.txt

# 5. Instal seluruh library Python dengan optimasi tanpa cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 6. Salin seluruh sisa berkas proyek (termasuk folder templates, static, models, dll.)
COPY . .

# 7. Berikan hak akses penuh ke folder proyek agar Flask bisa menulis database SQLite dan menyimpan gambar hasil deteksi
RUN chmod -R 777 /code

# 8. Perintah utama untuk menyalakan aplikasi kuis Anda
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
>>>>>>> b73cd00b7e0ae6d1410a1de57b403e897908a1fa
