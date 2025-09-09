# 🖼️ AI Image Captioning Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Una herramienta web avanzada para generar captions de imágenes usando múltiples modelos de IA**

[🚀 Características](#-características) • [📦 Instalación](#-instalación) • [🎯 Uso](#-uso) • [🤖 Modelos](#-modelos) • [📸 Capturas](#-capturas)

</div>

---

## ✨ Características

### 🎨 **Interfaz Web Moderna**
- 🌙 **Modo Claro/Oscuro** - Detección automática del tema del sistema
- 📱 **Responsive Design** - Funciona en desktop, tablet y móvil
- ⚡ **Tiempo Real** - Barra de progreso en vivo durante la generación
- 🎯 **2 Columnas** - Layout optimizado para mejor visualización

### 🤖 **5 Modelos de IA Especializados**
- **BLIP** - Modelo preciso para captioning detallado (Por defecto)
- **WD14** - Waifu Diffusion 1.4, excelente para arte/anime
- **BLIP-2** - Optimizado para Stable Diffusion 1.5
- **ViT-GPT2** - Modelo creativo con descripciones elaboradas

### 🔄 **Sistema de Carga Dinámica (NUEVO)**
- **Carga Bajo Demanda** - Los modelos se cargan solo cuando los necesitas
- **Gestión Inteligente de Memoria** - Solo un modelo en RAM/VRAM a la vez
- **Inicio Rápido** - La aplicación inicia en segundos, no minutos
- **Cambio Automático** - Descarga el modelo anterior al cambiar
- **Optimización de Recursos** - Reduce uso de RAM de 15-20GB a 3-5GB

### ⚙️ **Funcionalidades Avanzadas**
- 📁 **Procesamiento en Lote** - Sube múltiples imágenes simultáneamente
- ✏️ **Editor Integrado** - Edita captions con vista previa de imagen
- 🏷️ **Palabra Clave** - Agrega prefijos personalizados a los captions
- 📏 **Control de Longitud** - Especifica número mínimo de palabras
- 🖼️ **Redimensionado** - Resize automático manteniendo aspect ratio
- 📦 **Exportación ZIP** - Descarga imágenes redimensionadas + TXT + JSON

### 🎛️ **Controles Personalizables**
- 🔧 **Resoluciones Predefinidas** - 512x512, 720x720, 768x768, 1024x1024
- 🎯 **Selección de Modelo** - Cambia entre modelos según necesidad
- 📊 **Progreso en Vivo** - "Generando captions... 4 de 26"
- 💾 **Auto-carga** - Carga automática de resultados en editor

---

## 📦 Instalación

### 🔧 **Requisitos del Sistema**
- **Python**: 3.8 o superior
- **RAM**: 16GB+ recomendado (8GB mínimo)
- **GPU**: CUDA compatible (opcional, mejora velocidad)
- **Espacio**: 30-40GB para modelos

### 🚀 **Instalación Rápida**

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/ai-captioning-tool.git
cd ai-captioning-tool

# 2. Crear entorno virtual
python -m venv venv_caption
venv_caption\Scripts\activate  # Windows
# source venv_caption/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar aplicación (automático)
# El archivo config.json se crea automáticamente desde config.example.json
# Edita config.json y agrega tu API key de OpenRouter

# 5. Ejecutar aplicación
python app.py
```

### 🎮 **Scripts de Ejecución**

| Script | Descripción | Uso |
|--------|-------------|-----|
| `run_gpu_0.bat` | GPU 0 con carga dinámica | `run_gpu_0.bat` |
| `run_gpu_1.bat` | GPU 1 con carga dinámica | `run_gpu_1.bat` |
| `run_cpu.bat` | Solo CPU con carga dinámica | `run_cpu.bat` |
| `run_with_gpu.py` | Selector interactivo | `python run_with_gpu.py` |
| `check_dynamic_loading.py` | Diagnóstico del sistema | `python check_dynamic_loading.py` |

### 🧹 **Scripts de Limpieza**

| Script | Descripción | Uso |
|--------|-------------|-----|
| `cleanup_models.bat` | Limpieza básica | Elimina todos los modelos |
| `cleanup_models_advanced.bat` | Limpieza avanzada | Con estadísticas detalladas |
| `cleanup_selective.bat` | Limpieza selectiva | Elige qué modelos eliminar |

---

## 🎯 Uso

### 🌐 **Acceso Web**
1. Ejecuta la aplicación
2. Abre tu navegador en `http://localhost:5000`
3. ¡Comienza a generar captions!

### 📸 **Generar Captions**
1. **Selecciona Modelo** - Elige entre los 6 modelos disponibles
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

## 🤖 Modelos

### 📊 **Comparación de Modelos**

| Modelo | Tamaño | RAM | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----|-----------|---------|-----------------|
| **BLIP** | 1.2GB | 3GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Uso general** |
| **WD14** | 3GB | 6GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | Arte/anime |
| **BLIP-2** | 5GB | 8GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Stable Diffusion |
| **CLIP** | 1GB | 2GB | ⭐⭐⭐⭐⭐ | ⭐⭐ | Procesamiento masivo |
| **ViT-GPT2** | 2GB | 4GB | ⭐⭐⭐ | ⭐⭐⭐ | Captions creativos |

### 🎯 **Recomendaciones de Uso**

#### **Para Captioning General:**
- **BLIP** - Equilibrio perfecto velocidad/calidad
- **WD14** - Excelente para imágenes artísticas

#### **Para Stable Diffusion:**
- **BLIP-2** - Optimizado específicamente para SD 1.5

#### **Para Velocidad:**
- **CLIP** - El más rápido para lotes grandes
- **ViT-GPT2** - Creativo y elaborado

---

## 📸 Capturas de Pantalla

### 🌙 **Modo Oscuro**
![Modo Oscuro](docs/screenshots/dark-mode.png)
*Interfaz en modo oscuro con layout de 2 columnas*

### ☀️ **Modo Claro**
![Modo Claro](docs/screenshots/light-mode.png)
*Interfaz en modo claro con selección de modelos*

### ⚡ **Progreso en Tiempo Real**
![Progreso](docs/screenshots/progress.png)
*Barra de progreso mostrando "Generando captions... 4 de 26"*

---

## 🛠️ Configuración Avanzada

### 🔧 **Variables de Entorno**

```bash
# Forzar GPU específica
export CUDA_VISIBLE_DEVICES=0

# Modo debug
export DEBUG_MODE=true

# Deshabilitar warnings de symlinks (Windows)
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
```

### 📁 **Estructura de Archivos**

```
ai-captioning-tool/
├── 📁 templates/
│   └── index.html          # Interfaz web
├── 📁 uploads/             # Imágenes subidas
├── 📁 results/             # Resultados generados
├── 📄 app.py               # Aplicación principal
├── 📄 requirements.txt     # Dependencias
├── 📄 run_with_gpu.py      # Selector de GPU
├── 📄 cleanup_*.bat        # Scripts de limpieza
└── 📄 README.md            # Este archivo
```

### 🎛️ **Personalización**

#### **Agregar Nuevo Modelo:**
1. Importa el modelo en `app.py`
2. Agrega función de generación
3. Actualiza la interfaz web
4. Añade a la lista de modelos

#### **Modificar Interfaz:**
- **Tema**: Edita variables CSS en `templates/index.html`
- **Layout**: Modifica clases Bootstrap
- **Funcionalidad**: Actualiza JavaScript

---

## 🐛 Solución de Problemas

### ❌ **Errores Comunes**

#### **"CUDA no disponible"**
```bash
# Verificar instalación CUDA
nvidia-smi

# Instalar PyTorch con CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### **"Modelo no está disponible"**
```bash
# Limpiar cache y reinstalar
python cleanup_models.bat
pip install -r requirements.txt
```

#### **"Error 413 - File too large"**
- Reducir tamaño de imágenes
- Aumentar `MAX_CONTENT_LENGTH` en `app.py`

### 🔍 **Logs de Debug**

```bash
# Ejecutar con debug
python run_with_gpu.py --debug

# Ver logs detallados
python app.py 2>&1 | tee debug.log
```

---

## 🤝 Contribuir

### 🚀 **Cómo Contribuir**

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### 📋 **Ideas para Contribuir**

- 🎨 Nuevos modelos de captioning
- 🌍 Soporte multiidioma
- 📱 App móvil
- 🔌 API REST
- 📊 Métricas de calidad
- 🎯 Detección de objetos

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Hugging Face** - Por los modelos de IA
- **Salesforce** - Por BLIP y BLIP-2
- **QWEN Team** - Por QWEN2.5-VL
- **OpenAI** - Por CLIP
- **Bootstrap** - Por el framework CSS
- **Flask** - Por el framework web

---

## 📞 Contacto

**Desarrollador**: [Tu Nombre](https://github.com/tu-usuario)
**Email**: tu-email@ejemplo.com
**Proyecto**: [https://github.com/tu-usuario/ai-captioning-tool](https://github.com/tu-usuario/ai-captioning-tool)

---

<div align="center">

**⭐ Si te gusta este proyecto, ¡dale una estrella! ⭐**

![GitHub stars](https://img.shields.io/github/stars/tu-usuario/ai-captioning-tool?style=social)
![GitHub forks](https://img.shields.io/github/forks/tu-usuario/ai-captioning-tool?style=social)

</div>