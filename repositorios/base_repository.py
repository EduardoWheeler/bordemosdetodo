from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def listar(self) -> list:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def insertar(self, entidad) -> int:
        pass

    @abstractmethod
    def actualizar(self, entidad) -> bool:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass