# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# Instala Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto
COPY ./app/* /app/

# Crea el directorio uploads si no existe y dale permisos de escritura
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

COPY ./app/templates /app/templates
# Expone el puerto en el que corre Flask
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar la app
CMD ["flask", "run"]