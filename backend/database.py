import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection_pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME")
            )
            print("✅ Conexión a PostgreSQL establecida")
        except Exception as e:
            print(f"❌ Error al conectar a PostgreSQL: {e}")

    def get_connection(self):
        return self.connection_pool.getconn() if self.connection_pool else None

    def return_connection(self, connection):
        if self.connection_pool:
            self.connection_pool.putconn(connection)

    def close_all(self):
        if self.connection_pool:
            self.connection_pool.closeall()


db = Database()