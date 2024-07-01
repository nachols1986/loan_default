import pandas as pd
from sqlalchemy import create_engine

# Credenciales de la base de datos
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "192.168.0.47"
DB_PORT = "5432"
DB_NAME = "loan_default_db"

# Función para crear una conexión a la base de datos
def create_db_connection():
    print("Creando conexión a la db")
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine.connect()

# Función para ejecutar una consulta y mostrar los resultados
def execute_query(connection, query):
    try:
        df = pd.read_sql_query(query, connection)
        print(df)
    except Exception as e:
        print("Error al ejecutar la consulta:", e)

# Consultas SQL para verificar las hipótesis
queries = {
    "Hipotesis 1": {
        "descripcion": "Existe una relación entre el historial de transacciones y el incumplimiento de préstamos.",
        "query": """
            WITH loan_status AS (
                SELECT 
                    l.loan_id, 
                    l.status, 
                    l.account_id, 
                    CASE 
                        WHEN l.status IN ('B', 'D') THEN 1 
                        ELSE 0 
                    END AS is_default
                FROM loan l
            ),
            transaction_counts AS (
                SELECT 
                    t.account_id, 
                    COUNT(t.trans_id) AS transaction_count
                FROM transactions t
                GROUP BY t.account_id
            ),
            transaction_intervals AS (
                SELECT 
                    account_id, 
                    transaction_count, 
                    (transaction_count / 50) * 50 AS transaction_interval
                FROM transaction_counts
            ),
            default_rates AS (
                SELECT 
                    ti.transaction_interval, 
                    COUNT(ls.loan_id) AS total_loans, 
                    SUM(ls.is_default) AS total_defaults
                FROM loan_status ls
                JOIN transaction_intervals ti ON ls.account_id = ti.account_id
                GROUP BY ti.transaction_interval
            )
            SELECT 
                transaction_interval, 
                total_defaults, 
                total_loans, 
                (CAST(total_defaults AS FLOAT) / total_loans) * 100 AS default_rate_percentage
            FROM default_rates
            ORDER BY transaction_interval;
        """
    },
    "Hipotesis 2": {
        "descripcion": "Los clientes con un mayor número de préstamos tienen una mayor probabilidad de incumplir.",
        "query": """
            WITH client_loans AS (
                SELECT 
                    d.client_id, 
                    COUNT(l.loan_id) AS loan_count,
                    SUM(CASE 
                            WHEN l.status IN ('B', 'D') THEN 1 
                            ELSE 0 
                        END) AS default_count
                FROM loan l
                JOIN account a ON l.account_id = a.account_id
                JOIN disposition d ON a.account_id = d.account_id
                WHERE d.type = 'OWNER'
                GROUP BY d.client_id
            ),
            default_rates AS (
                SELECT 
                    loan_count, 
                    COUNT(client_id) AS total_clients, 
                    SUM(default_count) AS total_defaults
                FROM client_loans
                GROUP BY loan_count
            )
            SELECT 
                loan_count, 
                total_clients, 
                total_defaults, 
                (CAST(total_defaults AS FLOAT) / total_clients) * 100 AS default_rate_percentage
            FROM default_rates
            ORDER BY loan_count;
        """
    },
    "Hipotesis 3": {
        "descripcion": "La ubicación geográfica de los clientes influye en su probabilidad de incumplimiento.",
        "query": """
            WITH loan_status AS (
                SELECT 
                    l.loan_id, 
                    l.status, 
                    a.district_id, 
                    CASE 
                        WHEN l.status IN ('B', 'D') THEN 1 
                        ELSE 0 
                    END AS is_default
                FROM loan l
                JOIN account a ON l.account_id = a.account_id
            ),
            district_defaults AS (
                SELECT 
                    ls.district_id, 
                    COUNT(ls.loan_id) AS total_loans, 
                    SUM(ls.is_default) AS total_defaults
                FROM loan_status ls
                GROUP BY ls.district_id
            ),
            region_defaults AS (
                SELECT 
                    d.region, 
                    SUM(dd.total_loans) AS total_loans, 
                    SUM(dd.total_defaults) AS total_defaults
                FROM district_defaults dd
                JOIN demographic d ON dd.district_id = d.district_id
                GROUP BY d.region
            )
            SELECT 
                UPPER(region) AS region, 
                total_loans, 
                total_defaults, 
                (CAST(total_defaults AS FLOAT) / total_loans) * 100 AS default_rate_percentage
            FROM region_defaults
            ORDER BY default_rate_percentage DESC;
        """
    },
    "Hipotesis 4": {
        "descripcion": "Los clientes con tarjetas de crédito activas tienen menos probabilidades de incumplir.",
        "query": """
            WITH loan_status AS (
                SELECT 
                    l.loan_id, 
                    l.status, 
                    d.client_id,
                    CASE 
                        WHEN l.status IN ('B', 'D') THEN 1 
                        ELSE 0 
                    END AS is_default
                FROM loan l
                JOIN account a ON l.account_id = a.account_id
                JOIN disposition d ON a.account_id = d.account_id
                WHERE d.type = 'OWNER'
            ),
            client_credit_card_status AS (
                SELECT 
                    d.client_id,
                    CASE 
                        WHEN cc.card_id IS NOT NULL THEN 1 
                        ELSE 0 
                    END AS has_credit_card
                FROM disposition d
                LEFT JOIN credit_card cc ON d.disp_id = cc.disp_id
                WHERE d.type = 'OWNER'
            ),
            default_rates AS (
                SELECT 
                    cccs.has_credit_card, 
                    COUNT(ls.loan_id) AS total_loans, 
                    SUM(ls.is_default) AS total_defaults
                FROM loan_status ls
                JOIN client_credit_card_status cccs ON ls.client_id = cccs.client_id
                GROUP BY cccs.has_credit_card
            )
            SELECT 
                has_credit_card, 
                total_loans, 
                total_defaults, 
                (CAST(total_defaults AS FLOAT) / total_loans) * 100 AS default_rate_percentage
            FROM default_rates;
        """
    },
    "Hipotesis 5": {
        "descripcion": "La tasa de desempleo en el distrito del cliente está relacionada con su historial crediticio.",
        "query": """
            WITH loan_status AS (
                SELECT 
                    l.loan_id, 
                    l.status, 
                    a.district_id, 
                    CASE 
                        WHEN l.status IN ('B', 'D') THEN 1 
                        ELSE 0 
                    END AS is_default
                FROM loan l
                JOIN account a ON l.account_id = a.account_id
            ),
            district_defaults AS (
                SELECT 
                    ls.district_id, 
                    COUNT(ls.loan_id) AS total_loans, 
                    SUM(ls.is_default) AS total_defaults
                FROM loan_status ls
                GROUP BY ls.district_id
            ),
            unemployment_defaults AS (
                SELECT 
                    FLOOR(d.unemployment_rate_1996) AS unemployment_rate_group,
                    SUM(dd.total_loans) AS total_loans, 
                    SUM(dd.total_defaults) AS total_defaults
                FROM district_defaults dd
                JOIN demographic d ON dd.district_id = d.district_id
                GROUP BY FLOOR(d.unemployment_rate_1996)
            )
            SELECT 
                unemployment_rate_group, 
                total_loans, 
                total_defaults, 
                (CAST(total_defaults AS FLOAT) / total_loans) * 100 AS default_rate_percentage
            FROM unemployment_defaults
            ORDER BY unemployment_rate_group;
        """
    }
}


# Función principal
def main():
    # Crear una conexión a la base de datos
    connection = create_db_connection()
       
    for hypothesis, details in queries.items():
        print(f"Verificando {hypothesis}: {details['descripcion']}")
        result = pd.read_sql(details['query'], connection)
        
        # Imprimir resultados
        print("Resultados:")
        if not result.empty:
            print(result.to_string(index=False))
        else:
            print("No se encontraron resultados.")
            
        print("-" * 100)
        print("-" * 100)
        print() 

    # Cerrar la conexión
    connection.close()
    
if __name__ == "__main__":
    main()
