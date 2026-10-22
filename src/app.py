
import os
import time
import mysql.connector
from flask import Flask

app = Flask(__name__)

def conectar_mysql():
    for intento in range(30):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                port=3306,
                user=os.getenv("DB_USER", "hola_user"),
                password=os.getenv("DB_PASSWORD", "hola_password"),
                database=os.getenv("DB_NAME", "hola_mundo")
            )
        except mysql.connector.Error:
            time.sleep(2)
    raise Exception("No se pudo conectar a MySQL")

@app.route("/")
def hola_mundo():
    try:
        conexion = conectar_mysql()
        cursor = conexion.cursor()
        cursor.execute("SELECT 'Conexión a MySQL exitosa'")
        mensaje = cursor.fetchone()[0]
        cursor.close()
        conexion.close()

        return f"""
        <h1>¡Hola Mundo!</h1>
        <p>Aplicación web funcionando con Python y Flask.</p>
        <p>Base de datos: {mensaje}</p>
        """
    except Exception:
        return "Hola Mundo, pero no hay conexión con MySQL.", 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
