# Generador de Captions con IA - Docker

Esta carpeta contiene todos los archivos necesarios para ejecutar la aplicación en un contenedor Docker.

## Estructura

```
docker/
├── app/                    # Código de la aplicación
│   ├── app.py             # Aplicación principal Flask
│   ├── config.json        # Configuración centralizada (crear desde ejemplo)
│   ├── requirements.txt   # Dependencias Python (minimal)
│   ├── templates/         # Plantillas HTML
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   └── uploads/          # Directorio para imágenes subidas
├── Dockerfile            # Configuración de la imagen Docker
├── docker-compose.yml    # Orquestación de contenedores
├── .dockerignore         # Archivos a ignorar en el build
├── .gitignore           # Archivos a ignorar en Git
├── config.example.json  # Archivo de configuración de ejemplo
├── start.sh             # Script para iniciar la aplicación (Linux/Mac)
├── stop.sh              # Script para detener la aplicación (Linux/Mac)
└── README_DOCKER.md     # Este archivo
```

## Requisitos

- Docker Desktop instalado
- NVIDIA Docker (opcional, para aceleración GPU)
- API Key de OpenRouter (para el modelo Llama Vision)

## Configuración inicial

1. **El archivo `config.json` se crea automáticamente** desde `config.example.json` al iniciar el contenedor.

2. **Edita `app/config.json` y agrega tu API key de OpenRouter:**
   ```json
   {
     "api_keys": {
       "openrouter": "tu_api_key_aqui"
     }
   }
   ```

3. **Obtén tu API key de OpenRouter:**
   - Ve a https://openrouter.ai/
   - Regístrate o inicia sesión
   - Genera una API key
   - Cópiala en el archivo `config.json`

## Uso Rápido

### Iniciar la aplicación
```bash
# Opción 1: Usar el script (Linux/Mac)
./start.sh

# Opción 2: Comandos manuales
docker-compose build
docker-compose up -d
```

### Detener la aplicación
```bash
# Opción 1: Usar el script (Linux/Mac)
./stop.sh

# Opción 2: Comando manual
docker-compose down
```

### En Windows
Si estás en Windows, puedes usar directamente los comandos de Docker:
```cmd
docker-compose build
docker-compose up -d
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f
```

## Configuración

La aplicación se configura mediante el archivo `app/config.json`. Los cambios se reflejan automáticamente al reiniciar el contenedor.

### Variables de entorno importantes

- `CUDA_VISIBLE_DEVICES=0`: Especifica qué GPU usar (si está disponible)
- `FLASK_ENV=production`: Modo de producción

## Volúmenes

Los siguientes directorios se montan como volúmenes para persistir datos:

- `./app/uploads` → `/app/uploads` (imágenes subidas)
- `./app/static` → `/app/static` (archivos estáticos y captions)
- `./app/backups` → `/app/backups` (respaldos)
- `./app/config.json` → `/app/config.json` (configuración)

## Puertos

- **5000**: Puerto de la aplicación web (http://localhost:5000)

## Características

- ✅ Soporte para GPU NVIDIA (CUDA)
- ✅ Modelos BLIP, BLIP2 y Llama Vision
- ✅ Análisis de metadatos EXIF
- ✅ Interfaz web completa
- ✅ Sistema de configuración centralizado
- ✅ Persistencia de datos
- ✅ Health checks automáticos

## Solución de problemas

### Error de GPU
Si no tienes GPU NVIDIA o Docker no puede acceder a ella, la aplicación funcionará con CPU (más lento).

### Error de memoria
Si tienes problemas de memoria, puedes ajustar los límites en `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G
    reservations:
      memory: 2G
```

### Reconstruir la imagen
Si cambias el código, reconstruye la imagen:

```bash
docker-compose build --no-cache
docker-compose up -d
```

## Desarrollo

Para desarrollo, puedes montar el código como volumen:

```yaml
volumes:
  - ./app:/app
```

Esto permitirá cambios en tiempo real sin reconstruir la imagen.
