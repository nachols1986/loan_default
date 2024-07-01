import pandas as pd
from sqlalchemy import create_engine
import time
import requests
import io

# Credenciales de la base de datos
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "190.180.0.45"
DB_PORT = "5432"
DB_NAME = "loan_default_db"

# Función para crear una conexión a la base de datos
def create_db_connection():
    print("Creando conexión a la db")
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return engine.connect()

csv_files_ids = {
    "account": "107yz8aXM0aEq-t3JcEj7wie1_c2u0Hf3",
    "client": "106SG9mZ8tdTygSB84UREQd6vXDxjQzxe",
    "credit_card": "1011GeReswbrlcuLgER4LI_NRxAucKjjk",
    "demographic": "1-lYMhx-V5vsmnXx86H1oWbI66uyzKNZ_",
    "disposition": "1-bs0i9fgJGeZ81-rY6CUcnCXnPalaJFZ",
    "loan": "1-aIVFFBpOG456o7zKiwPcDH5DvnjbXL-",
    "orders": "1-_l8LVxRp-M5tgXa1nm3iXAbPVPmWOoT",
    "transactions": "1-Vv-UeGmpkuk_OuRkNqi8FuPD5sSeOMZ"
}

sql_files_ids = {
    "deactivate": "10Q3aKVqvXHT5eXA36O4ue3qgYhIHC5Rb",
    "reactivate": "10FKxHLuVDgIGJOlb2H93nMoaqLfhWjze"
}

# Lista de archivos CSV
csv_files = ["account.csv", "credit_card.csv", "client.csv", "disposition.csv", "demographic.csv", "loan.csv", "orders.csv", "transactions.csv"]

   
def download_file_from_google_drive(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    return response.content.decode('utf-8')

# Función para cargar los datos de los archivos CSV a la base de datos
def load_data_to_db(connection):
    # Define el orden de carga de las tablas
    table_order = ["demographic", "account", "client", "disposition", "credit_card", "loan", "transactions", "orders"]
    
    # Itera sobre cada tabla en el orden definido
    for table_name in table_order:
        # Obtener el ID del archivo CSV correspondiente a la tabla
        file_id = csv_files_ids[table_name]
        
        try:
            # Descargar el contenido del archivo CSV
            csv_content = download_file_from_google_drive(file_id)
            
            # Obtener los nombres de las columnas y tipos de datos de la tabla
            column_names_and_types = get_column_names_and_types(table_name)
            column_names = list(column_names_and_types.keys())  # Obtener los nombres de las columnas
            column_types = {col: "Int64" if dtype == int else dtype for col, dtype in column_names_and_types.items()}  # Tipos de datos, ajustando los int a "Int64"
            
            # Leer el archivo CSV utilizando los nombres de columnas y tipos de datos
            df = pd.read_csv(io.StringIO(csv_content), sep=";", skiprows=1, names=column_names, dtype=column_types, na_values=["?", "NA"])
            
            # Cargar los datos en la tabla correspondiente de la base de datos
            df.to_sql(table_name, connection, if_exists='append', index=False)
            print("Datos cargados correctamente en la tabla:", table_name)
            
        except Exception as e:
            print("Error al cargar datos en la tabla", table_name, ":", e)

# Función para descargar y ejecutar un archivo SQL desde Google Drive
def execute_sql_from_google_drive(connection, file_id):
    # Construir la URL para descargar el archivo desde Google Drive
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        sql_commands = response.text
        
        # Separar los comandos SQL por líneas
        sql_commands = sql_commands.split(';')
        
        # Eliminar los comentarios y líneas vacías
        sql_commands = [cmd.strip() for cmd in sql_commands if not cmd.startswith('--') and cmd.strip()]
        
        # Ejecutar los comandos SQL
        for cmd in sql_commands:
            try:
                connection.execute(cmd)
            except Exception as e:
                print("Error al ejecutar comando:", cmd)
                print("Error:", e)
                
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo SQL: {e}")
        
def get_column_names_and_types(table_name):
    # Definir los nombres de las columnas y tipos de datos para cada tabla
    column_names_and_types_dict = {
        "demographic": {"district_id": int, "name": str, "region": str, "num_inhabitants": int,
                        "num_municipalities_lt_499": int, "num_municipalities_500_1999": int,
                        "num_municipalities_2000_9999": int, "num_municipalities_gt_10000": int,
                        "num_cities": int, "urban_inhabitants_ratio": float, "avg_salary": float,
                        "unemployment_rate_1995": float, "unemployment_rate_1996": float,
                        "num_entrepreneurs_per_1000": float, "num_crimes_1995": float, "num_crimes_1996": float},
        "account": {"account_id": int, "district_id": int, "frequency": str, "date": int},
        "client": {"client_id": int, "birth_number": str, "district_id": int},
        "disposition": {"disp_id": int, "client_id": int, "account_id": int, "type": str},
        "credit_card": {"card_id": int, "disp_id": int, "type": str, "issued": str},
        "loan": {"loan_id": int, "account_id": int, "date": int, "amount": float, "duration": int,
                 "payments": float, "status": str},
        "transactions": {"trans_id": int, "account_id": int, "date": int, "type": str, "operation": str,
                         "amount": float, "balance": float, "k_symbol": str, "bank": str, "account": str},
        "orders": {"order_id": int, "account_id": int, "bank_to": str, "account_to": str, "amount": float,
                   "k_symbol": str}
    }
    return column_names_and_types_dict[table_name]

# Esperar a que el contenedor de la base de datos esté en funcionamiento
def wait_for_db_container():
    print("Esperando a que el contenedor de la base de datos esté en funcionamiento...")
    while True:
        try:
            connection = create_db_connection()
            print("¡El contenedor de la base de datos está en funcionamiento!")
            connection.close()
            break
        except Exception as e:
            print("Error:", e)
            print("Intentando nuevamente en 5 segundos...")
            time.sleep(5)


        
# Función principal
def main():
    # Esperar a que el contenedor de la base de datos esté en funcionamiento
    wait_for_db_container()
    
    # Crear una conexión a la base de datos
    connection = create_db_connection()
    
    # Desactivar las restricciones de llaves foráneas --> ya no hace falta porque se populan en orden
    # print("Desactivando restricciones de llaves foráneas...")
    # execute_sql_from_google_drive(engine, sql_files_ids["deactivate"])
    
    # Cargar los datos de los archivos CSV a la base de datos
    load_data_to_db(connection)
    
    # Reactivar restricciones de llaves foráneas --> ya no hace falta porque se populan en orden
    # print("Reactivando restricciones de llaves foráneas...")
    # execute_sql_from_google_drive(engine, sql_files_ids["reactivate"])
    
    # Cerrar la conexión
    connection.close()

if __name__ == "__main__":
    main()
