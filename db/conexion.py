import mysql.connector
from mysql.connector import Error
from config import ConfigDB

class Conexion:
    def __init__(self, config: ConfigDB | None = None):
        self._config = config or ConfigDB()
        self._cnx = None
    
    def __enter__(self):
        try:
            self._cnx = mysql.connector.connect(
                host=self._config.host,
                port=self._config.port,
                user=self._config.user,
                password=self._config.password,
                database=self._config.database,
            )
            self._cnx.autocommit = False
            return self._cnx
        except Error as e:
            raise ConnectionError(f"no se pudo conectar a myqsl: {e}") from e
    
    def __exit__(self, tipo_exc, exc, tb):
        if self._cnx is None:
            return False
        if tipo_exc is None:
            self._cnx.commit()
        else:
            self._cnx.rollback()
        self._cnx.close()
        return False