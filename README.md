# Signals Flask App

Este proyecto es una aplicación web construida con Flask que permite a los usuarios cargar imágenes o archivos PDF para extraer señales utilizando técnicas de procesamiento de imágenes y OCR.

## Estructura del Proyecto

```
signals-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   └── templates
│       └── index.html
├── requirements.txt
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

5. Instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

## Ejecución de la Aplicación

1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta la aplicación Flask:

   ```
   flask run
   ```

3. Abre tu navegador y ve a `http://127.0.0.1:5000/` para acceder a la aplicación.

## Uso

1. En la interfaz de usuario, utiliza el formulario para cargar una imagen o un archivo PDF.
2. Una vez cargado, la aplicación procesará el archivo y mostrará las señales capturadas en la página.

## Dependencias

Este proyecto utiliza las siguientes bibliotecas:

- Flask
- OpenCV
- pytesseract
- pdf2image
- numpy

Asegúrate de que todas las dependencias estén instaladas correctamente para que la aplicación funcione sin problemas.