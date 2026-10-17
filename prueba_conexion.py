from db.conexion import Conexion

with Conexion() as cnx:
    cur = cnx.cursor()
    cur.execute("select version(), database(), current_user()")
    print(cur.fetchone())