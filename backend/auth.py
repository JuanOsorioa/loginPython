from backend.database import db
import bcrypt

class Auth:
    @staticmethod
    def register_user(user_data):
        """Registra usuario y datos médicos"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar usuario
            cursor.execute("""
                INSERT INTO usuarios 
                (nombre_usuario, contrasena, primer_nombre, segundo_nombre, 
                 primer_apellido, segundo_apellido, fecha_nacimiento,
                 correo, celular, ubicacion, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                user_data["new_username"],
                bcrypt.hashpw(user_data["new_password"].encode(), bcrypt.gensalt()).decode(),
                user_data["primer_nombre"],
                user_data.get("segundo_nombre"),
                user_data["primer_apellido"],
                user_data.get("segundo_apellido"),
                user_data["fecha_nacimiento"],
                user_data["correo"],
                user_data["celular"],
                user_data["ubicacion"],
                user_data["direccion"]
            ))
            user_id = cursor.fetchone()[0]

            # 2. Insertar datos médicos
            cursor.execute("""
                INSERT INTO datos_medicos 
                (usuario_id, tipo_sangre, presion, estatura, peso, temperatura)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                user_data["tipo_sangre"],
                user_data["presion"],
                user_data["estatura"],
                user_data["peso"],
                user_data["temperatura"]
            ))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            db.return_connection(conn)
                        # ...existing code...
            
    @staticmethod
    def login_user(username, password):
        """Valida usuario y contraseña"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, contrasena FROM usuarios WHERE nombre_usuario = %s", (username,))
            row = cursor.fetchone()
            if row and bcrypt.checkpw(password.encode(), row[1].encode()):
                return {"id": row[0], "nombre_usuario": username}
            return None
        finally:
            cursor.close()
            db.return_connection(conn)