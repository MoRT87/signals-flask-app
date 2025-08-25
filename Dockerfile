# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instala dependencias del sistema y supervisor en una sola capa
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr poppler-utils ffmpeg libsm6 libxext6 supervisor \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo requirements.txt primero para aprovechar cache
COPY requirements.txt ./

# Instala dependencias de Python y limpia cache
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

# Copia el resto de la aplicación y archivos de configuración
COPY app/* /app/
COPY app/templates /app/templates
COPY cleanup_thumbnails.py /app/cleanup_thumbnails.py
COPY supervisord.conf /etc/supervisord.conf

# Crea el directorio uploads y thumbnails y da permisos
RUN mkdir -p /app/uploads/thumbnails && chmod -R 777 /app/uploads

# Expone el puerto de Flask
EXPOSE 5000

# Variables de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar supervisor, que lanzará Flask y el script de limpieza
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]