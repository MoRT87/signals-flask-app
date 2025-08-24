# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instala dependencias del sistema y limpia cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tesseract-ocr poppler-utils ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo requirements.txt primero para aprovechar cache
COPY requirements.txt ./

# Instala dependencias de Python y limpia cache
RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	&& rm -rf ~/.cache/pip

# Copia el resto de la aplicación
COPY ./app/* /app/

# Crea el directorio uploads y da permisos
RUN mkdir -p ./uploads && chmod +w ./uploads

# Copia las plantillas
COPY ./app/templates /app/templates

# Expone el puerto de Flask
EXPOSE 5000

# Variables de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar la app
CMD ["flask", "run"]