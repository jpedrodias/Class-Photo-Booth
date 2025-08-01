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
app.secret_key = os.getenv('FLASKAPP_SECRET_KEY', 'supersecretkey')
app.config['LOGIN_PIN'] = os.getenv('FLASKAPP_LOGIN_PIN', '1234')

# Configuração das pastas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOTOS_DIR = os.path.join(BASE_DIR, 'fotos')
THUMBS_DIR = os.path.join(BASE_DIR, 'thumbs')
ZIPS_DIR = os.path.join(BASE_DIR, 'zips')

# Certifique-se de que as pastas existem com permissões adequadas
def create_directories_with_permissions():
    for directory in [FOTOS_DIR, THUMBS_DIR, ZIPS_DIR]:
        try:
            os.makedirs(directory, exist_ok=True)
            # Tentar definir permissões apenas em sistemas Unix/Linux
            if os.name != 'nt':  # 'nt' é o Windows
                try:
                    os.chmod(directory, 0o777)
                except (PermissionError, OSError):
                    print(f"Aviso: Não foi possível definir permissões para {directory}")
        except PermissionError as e:
            print(f"Erro de permissão ao criar diretório {directory}: {e}")
        except Exception as e:
            print(f"Erro ao criar diretório {directory}: {e}")

create_directories_with_permissions()


def safe_makedirs(directory):
    """Cria diretórios de forma segura, compatível com Windows e Linux"""
    try:
        os.makedirs(directory, exist_ok=True)
        # Apenas tenta definir permissões em sistemas Unix/Linux
        if os.name != 'nt':
            try:
                os.chmod(directory, 0o777)
            except (PermissionError, OSError):
                pass  # Ignora erros de permissão silenciosamente
        return True
    except Exception as e:
        print(f"Erro ao criar diretório {directory}: {e}")
        return False


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
    return redirect(url_for('turmas'))

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
    turmas = []
    with open(os.path.join(BASE_DIR, 'alunos.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['turma'] not in turmas:
                turmas.append(row['turma'])
    return render_template('turmas.html', turmas=turmas)

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
    turma_dir = os.path.join(FOTOS_DIR, turma)
    files = [file for root, dirs, files in os.walk(turma_dir) for file in files]

    if not files:
        return "Nenhuma imagem disponível para download.", 400

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zipf:
        for file in files:
            zipf.write(os.path.join(turma_dir, file), arcname=file)
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, download_name=f'{turma}.zip')

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
    
    # Criar diretório da foto de forma segura
    if not safe_makedirs(os.path.dirname(photo_path)):
        return "Erro ao criar diretório para fotos.", 500

    try:
        with open(photo_path, 'wb') as photo_file:
            photo_file.write(BytesIO(base64.b64decode(image_data)).getvalue())
    except Exception as e:
        return f"Erro ao salvar foto: {e}", 500

    thumb_path = os.path.join(THUMBS_DIR, turma, f'{processo}.jpg')
    
    # Criar diretório da thumbnail de forma segura
    if not safe_makedirs(os.path.dirname(thumb_path)):
        return "Erro ao criar diretório para thumbnails.", 500

    with open(photo_path, 'rb') as photo_file:
        image = cv2.imdecode(np.frombuffer(photo_file.read(), np.uint8), cv2.IMREAD_COLOR)
        height, width, _ = image.shape
        min_dim = min(height, width)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        cropped_image = image[start_y:start_y + min_dim, start_x:start_x + min_dim]
        thumbnail = cv2.resize(cropped_image, (250, 250))
        cv2.imwrite(photo_path, cv2.imdecode(cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])[1], cv2.IMREAD_COLOR))
        cv2.imwrite(thumb_path, cv2.imdecode(cv2.imencode('.jpg', thumbnail, [cv2.IMWRITE_JPEG_QUALITY, 50])[1], cv2.IMREAD_COLOR))

    return "Foto enviada com sucesso.", 200

@app.route('/thumbs/<turma>/<processo>.jpg')
@no_cache
def get_thumbnail(turma, processo):
    thumb_path = os.path.join(THUMBS_DIR, turma, f'{processo}.jpg')
    if not os.path.exists(thumb_path):
        return send_file(os.path.join(BASE_DIR, 'static', 'student_icon.jpg'))
    return send_file(thumb_path)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == app.config['LOGIN_PIN']:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='PIN incorreto')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.before_request
def require_login():
    if not session.get('logged_in') and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
