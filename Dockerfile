# Dockerfile para Generador de Captions con IA
FROM python:3.9-slim-bullseye

# Metadatos
LABEL maintainer="Captioning AI Generator"
LABEL description="Generador de captions con IA usando BLIP, BLIP2 y Llama Vision"
LABEL version="1.0"
LABEL name="captioning-ai-generator"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY app/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip

# Instalar PyTorch con CUDA (versiones específicas que funcionan)
RUN pip install --no-cache-dir torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# Instalar ONNX Runtime GPU
RUN pip install --no-cache-dir onnxruntime-gpu

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ .

# Crear directorios necesarios
RUN mkdir -p uploads static/captions backups

# Exponer puerto
EXPOSE 5000

# Variables de entorno para la aplicación
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando por defecto
CMD ["python", "app.py"]

