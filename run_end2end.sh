#!/bin/bash

# Levantar el servidor PostgreSQL y el script de inicialización
docker-compose up -d

# Esperar a que PostgreSQL esté listo
while ! docker exec -it loan_default-db-1 pg_isready -U user -d loan_default_db; do
    echo "Esperando a que PostgreSQL esté listo..."
    sleep 5
done

# Construir la imagen para popular las tablas
docker build -t populate-image -f Dockerfile.populate .

# Ejecutar el contenedor para cargar los datos
docker run --network=loan_default_nw --ip=192.168.0.74 --rm populate-image

# Construir la imagen para el reporte
docker build -t reporting-image -f Dockerfile.reporting .

# Ejecutar el contenedor para generar el reporte
docker run --network=loan_default_nw --ip=192.168.0.74 --rm reporting-image

# Detener el servidor PostgreSQL al finalizar
docker-compose down
