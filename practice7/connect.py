import psycopg2
from config import load_config


def connect():
    try:
        conn = psycopg2.connect(**load_config())
        print("Connected successfully!")
        return conn
    except Exception as e:
        print(e)