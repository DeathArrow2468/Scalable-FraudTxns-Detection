import psycopg2
from psycopg2.extras import RealDictCursor

from config import *

class Database:
    @staticmethod
    def connect():
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode="require"
        )

    @staticmethod
    def cursor(conn):
        return conn.cursor(cursor_factory=RealDictCursor)