import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Clase para manejar la conexión a la base de datos
class Database:
    def __init__(self):
        self.connection_pool = None
        self._initialize_pool()

    # Inicializar el pool de conexiones
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

    # Obtener una conexión del pool
    def get_connection(self):
        return self.connection_pool.getconn() if self.connection_pool else None

    # Devolver una conexión al pool
    def return_connection(self, connection):
        if self.connection_pool:
            self.connection_pool.putconn(connection)

    # Cerrar todas las conexiones
    def close_all(self):
        if self.connection_pool:
            self.connection_pool.closeall()

    # Método para obtener resultados como diccionarios
    def fetch_as_dict(self, cursor, query, params=None):
        cursor.execute(query, params or ())
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Método para verificar la conexión a la base de datos
    def test_connection(self):
        """Verifica si la conexión a la base de datos es exitosa."""
        try:
            conn = self.get_connection()
            if conn:
                print("✅ Conexión a la base de datos verificada exitosamente.")
                self.return_connection(conn)
                return True
            else:
                print("❌ No se pudo establecer conexión con la base de datos.")
                return False
        except Exception as e:
            print(f"❌ Error al verificar la conexión: {e}")
            return False


# Instancia global de la base de datos
db = Database()