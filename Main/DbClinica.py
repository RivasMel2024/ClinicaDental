import mysql.connector
from mysql.connector import Error

def obtener_datos():
    try:
        print("📡 Intentando conectar a la base de datos...")
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307, 
            user='root',
            password='1234',
            database='clinicadental'
        )
        print("✅ Conectado correctamente.")

        cursor = conexion.cursor()
        print("🔍 Ejecutando consulta SQL...")
        cursor.execute("select Nombre from Paciente limit 2 ;")

        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        cursor.close()
        conexion.close()

        print("📦 Datos obtenidos correctamente.")
        return columnas, resultados

    except Error as e:
        print("❌ Error al conectar a MariaDB")
        print(e)
        return [], []
