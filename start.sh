#!/bin/bash

echo "========================================"
echo "  Generador de Captions con IA - Docker"
echo "========================================"
echo

echo "Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker no está instalado o no está en el PATH"
    echo "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "Docker encontrado!"
echo

echo "Construyendo la imagen de Docker..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al construir la imagen"
    exit 1
fi

echo
echo "Iniciando el contenedor..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al iniciar el contenedor"
    exit 1
fi

echo
echo "========================================"
echo "  Aplicación iniciada correctamente!"
echo "========================================"
echo
echo "La aplicación está disponible en: http://localhost:5000"
echo
echo "Para ver los logs: docker-compose logs -f"
echo "Para detener: docker-compose down"
echo "Para reiniciar: docker-compose restart"
echo
