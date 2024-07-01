# ITBA - Cloud Data Engineering

Este repositorio contiene un análisis de datos sobre préstamos bancarios utilizando datos de un banco checo. 

## Descripción del Dataset

Para una descripción detallada del dataset utilizado y el modelo de base de datos empleado, consulte el archivo [Descripcion_dataset.md](Descripcion_dataset.md). También puede visualizar el diagrama del modelo de base de datos en [dbdiagram.io](https://dbdiagram.io/d/Czech-Bank-64fa1cd002bd1c4a5e2b48a2).

## Resolución de los Ejercicios

### Consultas SQL Realizadas

1. **Relación entre el historial de transacciones y el incumplimiento de préstamos**
   - Consulta para ver la cantidad de transacciones en filas y el % de default (status C y D).

2. **Clientes con un mayor número de préstamos y su probabilidad de incumplir**
   - Consulta para verificar si los clientes con más préstamos tienen una mayor probabilidad de incumplir.

3. **Influencia de la ubicación geográfica en la probabilidad de incumplimiento**
   - Consulta para evaluar si la ubicación geográfica (región) influye en la probabilidad de incumplimiento de los clientes.

4. **Clientes con tarjetas de crédito activas y su probabilidad de incumplir**
   - Consulta para analizar si los clientes con tarjetas de crédito activas tienen menos probabilidades de incumplir.

5. **Relación entre la tasa de desempleo y el historial crediticio del cliente**
   - Consulta para investigar si la tasa de desempleo en el distrito del cliente está relacionada con su historial crediticio.

### Ejecución End-to-End con BASH Script

Para ejecutar todo el proceso de extremo a extremo, asegúrese de tener Docker instalado y siga los siguientes pasos:

1. Clone este repositorio:

   ```bash
   git clone https://github.com/nachols1986/loan_default.git
   cd loan_default

2. Ejecute el script run_end2end.sh: este script maneja la construcción de imágenes Docker, la carga de datos en la base de datos y la generación de reportes, asegurando que todo el proceso sea automatizado y reproducible:

    ```
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
    ```