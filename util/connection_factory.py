import psycopg2
from psycopg2 import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='chris',
            password='',  # removed password for security reasons uploading to GitHub
            host='',
            port='5432'

        )
        return conn
    except OperationalError as e:
        print(f"{e}")
        return conn


connection = create_connection()
