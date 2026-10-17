from db.conexion import Conexion
from modelos.parche import Parche
from repositorios.base_repository import BaseRepository

class ParcheRepository(BaseRepository):
    @staticmethod
    def _a_objeto(fila: dict) -> Parche:
        return Parche(**fila)

    def listar(self) -> list[Parche]:
        sql = ("SELECT id_parche AS id, nombre, descripcion, precio, stock, "
                "categoria_id, es_personalizado "
                "FROM parche ORDER BY nombre")
        with Conexion() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql)
            return [self._a_objeto(f) for f in cur.fetchall()]

    def buscar_por_id(self, id: int) -> Parche | None:
        sql = ("SELECT id_parche AS id, nombre, descripcion, precio, stock, "
                "categoria_id, es_personalizado "
                "FROM parche WHERE id_parche = %s")
        with Conexion() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, (id,))
            fila = cur.fetchone()
            return self._a_objeto(fila) if fila else None

    def insertar(self, parche: Parche) -> int:
        sql = ("INSERT INTO parche (nombre, descripcion, precio, stock, categoria_id, es_personalizado) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
        datos = (parche.nombre, parche.descripcion, parche.precio,
                parche.stock, parche.categoria_id, parche.es_personalizado)
        with Conexion() as cnx:
            cur = cnx.cursor()
            cur.execute(sql, datos)
            parche.id = cur.lastrowid
            return parche.id

    def actualizar(self, parche: Parche) -> bool:
        sql = ("UPDATE parche SET nombre=%s, descripcion=%s, precio=%s, "
                "stock=%s, categoria_id=%s, es_personalizado=%s WHERE id_parche=%s")
        datos = (parche.nombre, parche.descripcion, parche.precio,
                parche.stock, parche.categoria_id, parche.es_personalizado, parche.id)
        with Conexion() as cnx:
            cur = cnx.cursor()
            cur.execute(sql, datos)
            return cur.rowcount == 1

    def eliminar(self, id: int) -> bool:
        sql = "DELETE FROM parche WHERE id_parche = %s"
        with Conexion() as cnx:
            cur = cnx.cursor()
            cur.execute(sql, (id,))
            return cur.rowcount == 1


if __name__ == "__main__":
    repo = ParcheRepository()
    
    nuevo_parche = Parche(
        nombre="iron maiden",
        precio=2800,
        stock=15,
        categoria_id=1,
        descripcion="edicion especial"
    )
    
    id_creado = repo.insertar(nuevo_parche)
    print(f"parche creado con id: {id_creado}")
    
    parches = repo.listar()
    print("lista de parches")
    for p in parches:
        print(p)
    
    parche = repo.buscar_por_id(id_creado)
    if parche:
        print(f"encontrado: {parche.nombre}")
        
        parche.precio = 3200
        modificado = repo.actualizar(parche)
        print(f"actualizado: {modificado}")