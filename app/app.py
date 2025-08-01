from flask import Flask, render_template, request, redirect, url_for, send_file, session, Response, make_response
import os
import csv
import zipfile
from io import BytesIO
import cv2
import base64
import numpy as np
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para usar sessões

# Configuração das pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOTOS_DIR = os.path.join(BASE_DIR, 'fotos')
THUMBS_DIR = os.path.join(BASE_DIR, 'thumbs')
ZIPS_DIR = os.path.join(BASE_DIR, 'zips')

# Certifique-se de que as pastas existem
os.makedirs(FOTOS_DIR, exist_ok=True)
os.makedirs(THUMBS_DIR, exist_ok=True)
os.makedirs(ZIPS_DIR, exist_ok=True)


def no_cache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, str):
            response = make_response(response)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview')
def preview():
    return "Acesso à câmera agora é gerenciado pelo navegador.", 200

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filepath = os.path.join(BASE_DIR, 'alunos.csv')
        file.save(filepath)
        return redirect(url_for('turmas'))

@app.route('/turmas')
def turmas():
    turmas = set()
    with open(os.path.join(BASE_DIR, 'alunos.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            turmas.add(row['turma'])
    return render_template('turmas.html', turmas=sorted(turmas))

@app.route('/turma/<nome>')
@no_cache
def turma(nome):
    alunos = []
    with open(os.path.join(BASE_DIR, 'alunos.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['turma'] == nome:
                alunos.append(row)
    return render_template('turma.html', turma=nome, alunos=alunos)

@app.route('/download/<turma>')
def download_zip(turma):
    zip_path = os.path.join(ZIPS_DIR, f'{turma}.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        turma_dir = os.path.join(FOTOS_DIR, turma)
        for root, dirs, files in os.walk(turma_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    return send_file(zip_path, as_attachment=True)

@app.route('/take_photo/<turma>/<processo>')
def take_photo(turma, processo):
    return "A captura de fotos agora é gerenciada pelo navegador.", 200

@app.route('/capture_photo/<turma>/<processo>')
def capture_photo(turma, processo):
    return render_template('capture_photo.html', turma=turma, processo=processo)

@app.route('/upload_photo/<turma>/<processo>', methods=['POST'])
def upload_photo(turma, processo):
    data = request.get_json()
    if not data or 'image' not in data:
        return "Dados inválidos.", 400

    image_data = data['image'].split(',')[1]
    photo_path = os.path.join(FOTOS_DIR, turma, f'{processo}.jpg')
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)

    with open(photo_path, 'wb') as photo_file:
        photo_file.write(BytesIO(base64.b64decode(image_data)).getvalue())

    thumb_path = os.path.join(THUMBS_DIR, turma, f'{processo}.jpg')
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

    with open(photo_path, 'rb') as photo_file:
        image = cv2.imdecode(np.frombuffer(photo_file.read(), np.uint8), cv2.IMREAD_COLOR)
        height, width, _ = image.shape
        min_dim = min(height, width)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        cropped_image = image[start_y:start_y + min_dim, start_x:start_x + min_dim]
        thumbnail = cv2.resize(cropped_image, (250, 250))
        cv2.imwrite(thumb_path, thumbnail)

    return "Foto enviada com sucesso.", 200

@app.route('/thumbs/<turma>/<processo>.jpg')
@no_cache
def get_thumbnail(turma, processo):
    thumb_path = os.path.join(THUMBS_DIR, turma, f'{processo}.jpg')
    if not os.path.exists(thumb_path):
        return send_file(os.path.join(BASE_DIR, 'static', 'student_icon.jpg'))
    return send_file(thumb_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
