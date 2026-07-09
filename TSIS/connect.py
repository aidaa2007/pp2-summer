
import psycopg2
from config import load_config


def get_connection():
    params = load_config()

    try:
        conn = psycopg2.connect(**params)
        return conn

    except Exception as error:
        print("Connection error:")
        print(error)
        return None
