# Generador de Captions con IA

Una aplicación web moderna para generar captions automáticos de imágenes usando modelos de IA avanzados como BLIP, BLIP2 y Llama Vision.

## 🚀 Características

- **Múltiples modelos de IA**: BLIP, BLIP2 (local) y Llama Vision (remoto)
- **Análisis de metadatos**: Extracción automática de metadatos EXIF y ComfyUI
- **Interfaz moderna**: Diseño responsive con modo oscuro/claro
- **Arrastrar y soltar**: Subida fácil de imágenes
- **Zoom y pan**: Visualización interactiva de imágenes
- **Configuración centralizada**: Panel de configuración web
- **Dockerizado**: Fácil despliegue con Docker

## 🐳 Instalación con Docker

### Requisitos previos

- Docker Desktop instalado
- NVIDIA Docker (opcional, para aceleración GPU)
- API Key de OpenRouter (para el modelo Llama Vision)

### Configuración

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Configura la API key:**
   ```bash
   cp config.example.json app/config.json
   ```
   
   Edita `app/config.json` y agrega tu API key de OpenRouter:
   ```json
   {
     "api_keys": {
       "openrouter": "tu_api_key_aqui"
     }
   }
   ```

3. **Inicia la aplicación:**
   ```bash
   # Linux/Mac
   ./start.sh
   
   # Windows
   docker-compose up -d
   ```

4. **Accede a la aplicación:**
   - Abre http://localhost:5000 en tu navegador

### Comandos útiles

```bash
# Iniciar
docker-compose up -d

# Detener
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart
```

## 📋 Uso

1. **Sube una imagen** arrastrando y soltando o usando el botón de selección
2. **Selecciona un modelo** de IA (BLIP, BLIP2 o Llama Vision)
3. **Genera el caption** haciendo clic en "Generar Caption"
4. **Analiza metadatos** usando la pestaña de metadatos
5. **Configura la aplicación** usando la pestaña de configuración

## 🔧 Configuración

La aplicación se configura mediante el archivo `app/config.json`:

- **API Keys**: Configuración de servicios externos
- **Modelos**: Configuración de modelos de IA
- **Servidor**: Configuración del servidor web
- **Límites**: Límites de archivos y tamaño
- **Calidad**: Configuración de calidad de imágenes

## 🛠️ Desarrollo

### Estructura del proyecto

```
docker/
├── app/                    # Aplicación Flask
│   ├── app.py             # Aplicación principal
│   ├── config.json        # Configuración (crear desde ejemplo)
│   ├── requirements.txt   # Dependencias Python
│   ├── templates/         # Plantillas HTML
│   └── static/           # Archivos estáticos
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación
├── config.example.json   # Configuración de ejemplo
└── README.md            # Este archivo
```

### Modelos soportados

- **BLIP**: Modelo local para captions básicos
- **BLIP2**: Modelo local mejorado con mejor calidad
- **Llama Vision**: Modelo remoto de alta calidad (requiere API key)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema
