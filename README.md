
# Signals Flask App

Esta aplicación web permite a los usuarios cargar imágenes o archivos PDF para extraer información mediante procesamiento de imágenes y OCR con Google Gen AI (gemini-2.5-flash), utilizando Flask con soporte para vistas asíncronas. Incluye limpieza automática de miniaturas y soporte para ejecución en Docker con variables de entorno configurables.

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

## Variables de entorno

Puedes configurar variables de entorno para personalizar la app, por ejemplo:

```
GENAI_API_KEY=your_api_key
GENAI_MODEL=gemini-2.5-flash
FLASK_DEBUG=1
```

Al usar Docker, puedes pasarlas con `-e` o un archivo `.env`.

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
   docker build -t signals.
   ```

2. Ejecuta el contenedor con variables de entorno:

   ```
   docker run --restart=always -d -e GENAI_API_KEY=your_api_key -p 5000:5000 signals
   ```

   O usando un archivo `.env`:

   ```
   docker run --env-file .env -p 5000:5000 signals
   ```

3. Abre tu navegador y ve a `http://localhost:5000/`.


## Uso

1. En la interfaz web, utiliza el formulario para cargar una imagen.
2. La aplicación procesará el archivo y mostrará las señales extraídas.


## Dependencias

- Flask (con soporte async)
- OpenCV
- pdf2image
- numpy
- poppler-utils (sistema)
- ffmpeg (sistema)
- supervisor (solo Docker)

Asegúrate de instalar las dependencias del sistema si usas la app fuera de Docker.

## Limpieza automática de miniaturas

Las miniaturas generadas se almacenan en `uploads/thumbnails` y se eliminan automáticamente después de 10 minutos mediante un proceso de limpieza que corre en segundo plano dentro del contenedor Docker.
