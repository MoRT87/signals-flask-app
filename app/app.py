from flask import Flask, render_template, request, redirect, url_for, abort
import os
import shutil
import uuid
from .utils import extract_signals_from_file
import lmstudio as lms

app = Flask(__name__, static_url_path="/uploads", static_folder="uploads")

lms.configure_default_client(os.getenv("LMS_HOST", "http://localhost:1234"))
# Configuración de la aplicación
app.config["UPLOAD_FOLDER"] = "uploads"  # Carpeta para guardar imágenes subidas
app.config["MAX_CONTENT_LENGTH"] = (
    16 * 1024 * 1024
)  # Limitar el tamaño de archivo a 16 MB

# Registro de rutas


@app.route("/", methods=["GET", "POST"])
async def index():
    signals = []
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Crear subcarpeta única para este request
            request_id = str(uuid.uuid4())
            request_folder = os.path.join("uploads", request_id)
            os.makedirs(request_folder, exist_ok=True)
            file_path = os.path.join(request_folder, file.filename)
            file.save(file_path)

            try:
                signals = await extract_signals_from_file(file_path, request_folder)
            except Exception as e:
                app.logger.error(f" {e}")
                raise e
            finally:
                # Limpia la subcarpeta completa después de procesar
                shutil.rmtree(request_folder, ignore_errors=True)
    return render_template("index.html", signals=signals)
