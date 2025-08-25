# Signals Flask App

Esta aplicación web permite a los usuarios cargar imágenes o archivos PDF para extraer señales mediante procesamiento de imágenes y OCR, utilizando Flask con soporte para vistas asíncronas.

## Estructura del Proyecto

```
signals-flask-app
├── app
│   ├── __init__.py
│   ├── app.py
│   ├── utils.py
│   └── templates
│       └── index.html
├── requirements.txt
├── Dockerfile
└── README.md
```

## Instalación

1. Clona el repositorio o descarga los archivos del proyecto.
2. Navega al directorio del proyecto.
3. Crea un entorno virtual (opcional pero recomendado):

   ```
   python -m venv venv
   ```

4. Activa el entorno virtual:

   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Instala las dependencias (incluyendo soporte async para Flask):

   ```
   pip install -r requirements.txt
   ```

   O manualmente:

   ```
   pip install "flask[async]" opencv-python pytesseract pdf2image numpy
   ```

## Ejecución de la Aplicación

### Local

1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta la aplicación Flask:

   ```
   flask run
   ```

3. Abre tu navegador y ve a `http://127.0.0.1:5000/`.

### Con Docker

1. Construye la imagen Docker:

   ```
   docker build -t signals .
   ```

2. Ejecuta el contenedor y accede a su shell si lo deseas:

   ```
   docker run --restart=always -d -e "LMS_HOST=http://localhost:1234" --p 5000:5000 signals
   ```


## Uso

1. En la interfaz web, utiliza el formulario para cargar una imagen o PDF.
2. La aplicación procesará el archivo y mostrará las señales extraídas.

## Dependencias

- Flask (con soporte async)
- OpenCV
- pytesseract
- pdf2image
- numpy
- tesseract-ocr (sistema)
- poppler-utils (sistema)
- ffmpeg (sistema)

Asegúrate de instalar las dependencias del sistema si usas la app fuera de un contenedor Docker.