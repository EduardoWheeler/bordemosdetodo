from db.conexion import Conexion

if __name__ == "__main__":
    print("Probando conexión a la base de datos...")
    try:
        with Conexion() as cnx:
            with cnx.cursor() as cur:
                cur.execute("SELECT VERSION(), DATABASE(), CURRENT_USER()")
                resultado = cur.fetchone()
                print("¡Conexión exitosa!")
                print(f"Versión MySQL: {resultado[0]}")
                print(f"Base de datos activa: {resultado[1]}")
                print(f"Usuario conectado: {resultado[2]}")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")