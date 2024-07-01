#!/bin/bash

echo "listen_addresses = '192.168.0.47'" >> /var/lib/postgresql/data/postgresql.conf
#echo "listen_addresses = '*'" >> /var/lib/postgresql/data/postgresql.conf

echo "host loan_default_db user 192.168.0.0/24 scram-sha-256" >> /var/lib/postgresql/data/pg_hba.conf

docker-entrypoint.sh postgres

# Variables
DB_USER="user"
DB_NAME="loan_default_db"

# Esperar a que PostgreSQL esté listo
wait_for_postgres() {
    echo "Esperando a que PostgreSQL esté listo..."
    while true; do
        if pg_isready -U $DB_USER -d $DB_NAME; then
            echo "¡PostgreSQL está listo!"
            break
        else
            echo "Intentando nuevamente en 5 segundos..."
            sleep 5
        fi
    done
}

# Esperar a que PostgreSQL esté listo
wait_for_postgres

# Ejecutar las sentencias SQL para eliminar tablas existentes
echo "Eliminando tablas existentes si es que existen..."
psql -U $DB_USER -d $DB_NAME -c "DROP TABLE IF EXISTS account, client, disposition, credit_card, demographic, loan, orders, transactions;"

# Ejecutar las sentencias SQL para crear las nuevas tablas
echo "Creando nuevas tablas..."
psql -U $DB_USER -d $DB_NAME -c "
-- Crear tabla ACCOUNT
CREATE TABLE account (
    account_id INTEGER PRIMARY KEY,
    district_id INTEGER NOT NULL,
    frequency VARCHAR(20),
    date INTEGER -- Formato YYMMDD
);

-- Crear tabla CLIENT
CREATE TABLE client (
    client_id INTEGER PRIMARY KEY,
    birth_number VARCHAR(20), -- Formato YYMMDD
    district_id INTEGER
);

-- Crear tabla DISPOSITION
CREATE TABLE disposition (
    disp_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    type VARCHAR(20),
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Crear tabla LOAN
CREATE TABLE loan (
    loan_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    date INTEGER, -- Formato YYMMDD 
    amount NUMERIC(15, 2),
    duration INTEGER,
    payments NUMERIC(15, 2),
    status CHAR(1) CHECK (status IN ('A', 'B', 'C', 'D')), -- Solo valores A, B, C y D
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Crear tabla ORDER
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    bank_to CHAR(2),
    account_to VARCHAR(20),
    amount NUMERIC(15, 2),
    k_symbol VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Crear tabla TRANSACTION
CREATE TABLE transactions (
    trans_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL,
    date INTEGER, -- Formato YYMMDD
    type VARCHAR(20),
    operation VARCHAR(20),
    amount NUMERIC(15, 2),
    balance NUMERIC(15, 2),
    k_symbol VARCHAR(20),
    bank CHAR(2),
    account VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Crear tabla DEMOGRAPHIC
CREATE TABLE demographic (
    district_id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    region VARCHAR(50),
    num_inhabitants INTEGER,
    num_municipalities_lt_499 INTEGER,
    num_municipalities_500_1999 INTEGER,
    num_municipalities_2000_9999 INTEGER,
    num_municipalities_gt_10000 INTEGER,
    num_cities INTEGER,
    urban_inhabitants_ratio NUMERIC(5, 2),
    avg_salary NUMERIC(15, 2),
    unemployment_rate_1995 NUMERIC(5, 2),
    unemployment_rate_1996 NUMERIC(5, 2),
    num_entrepreneurs_per_1000 INTEGER,
    num_crimes_1995 INTEGER,
    num_crimes_1996 INTEGER
);

-- Crear tabla CREDIT CARD
CREATE TABLE credit_card (
    card_id INTEGER PRIMARY KEY,
    disp_id INTEGER NOT NULL,
    type VARCHAR(10),
    issued VARCHAR(30), -- Formato YYMMDD
    FOREIGN KEY (disp_id) REFERENCES disposition(disp_id)
);
"

# Verificar si las sentencias se ejecutaron correctamente
if [ $? -eq 0 ]; then
    echo "Tablas creadas correctamente en la base de datos."
else
    echo "Error al crear las tablas en la base de datos." >&2
    exit 1
fi
