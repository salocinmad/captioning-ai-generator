# 🐳 Docker - AI Image Captioning Tool

<div align="center">

![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Despliegue Docker del generador de captions con IA**

[🚀 Instalación](#-instalación) • [🎯 Uso](#-uso) • [🔧 Configuración](#-configuración) • [🛠️ Solución de Problemas](#️-solución-de-problemas)

</div>

---

## 🆕 **Cambios Recientes (Septiembre 2025)**

### ✅ **Mejoras Implementadas**
- **Python 3.12** - Actualizado desde Python 3.9
- **Transformers 4.56.1** - Versión estable actualizada
- **BLIP2 Modelo** - Cambiado a `flan-t5-xl` con `device_map="auto"`
- **Barra de Progreso** - Mejorada con progreso de imágenes (1 de 5, 2 de 5, etc.)
- **Interfaz Limpia** - Ocultados nombres de archivos, solo muestra contador
- **Mensajes Simplificados** - "Cargando modelo en memoria..." unificado

### 🔧 **Correcciones Técnicas**
- **Error BLIP2** - Solucionado "Cannot copy out of meta tensor"
- **Compatibilidad** - `use_safetensors=True` mantenido para BLIP
- **Dependencias** - Sincronizadas entre local y Docker
- **Progreso** - Arreglado cálculo de porcentajes

### 🐳 **Mejoras Docker**
- **Base Image** - `python:3.12-slim-bookworm`
- **Dependencias** - Versiones actualizadas y compatibles
- **GPU Support** - NVIDIA Docker optimizado
- **Volúmenes** - Persistencia de datos mejorada

---

## 🚀 **Instalación Docker**

### 🔧 **Requisitos**
- **Docker Desktop** instalado
- **NVIDIA Docker** (opcional, para GPU)
- **8GB RAM** mínimo (16GB recomendado)
- **15GB espacio** libre

### 📥 **Clonar y Ejecutar**

```bash
# 1. Clonar el repositorio
git clone https://github.com/salocinmad/captioning-ai-generator.git
cd captioning-ai-generator/docker

# 2. Configurar API key (opcional)
cp app/config.example.json app/config.json
# Editar app/config.json con tu API key de OpenRouter

# 3. Construir y ejecutar
docker-compose build
docker-compose up -d

# 4. Acceder a la aplicación
# http://localhost:5000
```

### 🎮 **Comandos Docker**

```bash
# Construir imagen
docker-compose build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reconstruir sin cache
docker-compose build --no-cache
```

---

## 🎯 **Uso**

### 🌐 **Acceso**
1. Ejecuta `docker-compose up -d`
2. Abre `http://localhost:5000`
3. ¡Comienza a generar captions!

### 📸 **Generar Captions**
1. **Selecciona Modelo** - Elige entre los 3 modelos disponibles
2. **Sube Imágenes** - Arrastra y suelta o haz clic para seleccionar
3. **Configura Opciones**:
   - 🏷️ Palabra clave (opcional)
   - 📏 Palabras mínimas (opcional)
4. **Genera** - Haz clic en "Generar Captions"
5. **Descarga** - Guarda resultados en ZIP

### ✏️ **Editar Captions**
1. Ve a la pestaña "Editar Captions"
2. Carga un archivo JSON de resultados
3. Edita cada caption individualmente
4. Guarda los cambios

---

## 🤖 **Modelos Disponibles**

### 📊 **3 Modelos de IA**

| Modelo | Tamaño | RAM | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----|-----------|---------|-----------------|
| **BLIP** | 1.2GB | 3GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Uso general** |
| **BLIP-2** | 5GB | 8GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Stable Diffusion |
| **Llama 3.2 Vision** | API | 0GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Máxima calidad** |

### 🎯 **Recomendaciones**

- **BLIP** - Equilibrio perfecto velocidad/calidad
- **BLIP-2** - Optimizado para Stable Diffusion 1.5
- **Llama 3.2 Vision** - API remota con prompts personalizados

---

## 🔧 **Configuración**

### 📁 **Estructura Docker**

```
docker/
├── app/                    # Aplicación completa
│   ├── app.py             # Backend Flask
│   ├── config.json        # Configuración
│   ├── requirements.txt   # Dependencias
│   ├── templates/         # Frontend
│   └── static/           # Archivos estáticos
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación
└── README_DOCKER.md     # Documentación Docker
```

### 🔧 **Variables de Entorno**

```bash
# GPU específica
CUDA_VISIBLE_DEVICES=0

# Modo debug
DEBUG_MODE=true

# Deshabilitar warnings
HF_HUB_DISABLE_SYMLINKS_WARNING=1
```

### 📦 **Volúmenes Persistentes**

- `./app/uploads` → `/app/uploads` (imágenes subidas)
- `./app/static` → `/app/static` (archivos estáticos)
- `./app/backups` → `/app/backups` (respaldos)
- `./app/config.json` → `/app/config.json` (configuración)

---

## 🛠️ **Solución de Problemas**

### ❌ **Errores Comunes**

#### **"CUDA no disponible"**
```bash
# Verificar GPU
nvidia-smi

# Verificar Docker GPU
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

#### **"Error de memoria"**
```bash
# Ajustar límites en docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4G
```

#### **"Modelo no carga"**
```bash
# Ver logs del contenedor
docker-compose logs -f

# Reconstruir imagen
docker-compose build --no-cache
```

### 🔍 **Logs y Debug**

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Acceder al contenedor
docker exec -it captioning-ai-generator bash

# Verificar espacio
docker exec -it captioning-ai-generator df -h
```

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT.

---

## 🙏 **Agradecimientos**

- **Hugging Face** - Por los modelos de IA
- **Salesforce** - Por BLIP y BLIP-2
- **Meta** - Por Llama 3.2 Vision
- **Docker** - Por la containerización

---

<div align="center">

**⭐ Si te gusta este proyecto, ¡dale una estrella! ⭐**

![GitHub stars](https://img.shields.io/github/stars/salocinmad/captioning-ai-generator?style=social)

</div>
