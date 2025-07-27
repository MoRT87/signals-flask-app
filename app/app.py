from flask import Flask, render_template, request, redirect, url_for
import os
from .utils import extract_signals_from_file


app = Flask(__name__, static_url_path='/uploads', static_folder="uploads")
    
# Configuración de la aplicación
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta para guardar imágenes subidas
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar el tamaño de archivo a 16 MB

# Registro de rutas



@app.route('/', methods=['GET', 'POST'])
def index():
    signals = []
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            signals = extract_signals_from_file(file_path)
           # os.remove(file_path)  # Clean up the uploaded file after processing
    return render_template('index.html', signals=signals)