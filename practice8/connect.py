import psycopg2

DB_NAME = "phonebook"
DB_USER = "postgres"
DB_PASSWORD = "Asd05052007@"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )