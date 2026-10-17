from dataclasses import dataclass

@dataclass
class Parche:
    nombre: str
    precio: int
    stock: int
    categoria_id: int
    descripcion: str | None = None
    es_personalizado: bool = False
    id: int | None = None

    def __post_init__(self):
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre del parche no puede estar vacío.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.nombre = self.nombre.strip().title()

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - ${self.precio} (Stock: {self.stock})"


if __name__ == "__main__":
    parche_1 = Parche(nombre= " misfits ", precio=1500, stock= 10, categoria_id=1, id=1)
    print(parche_1)
    
    try:
        parche_2 = Parche(nombre="ramones", precio=-500, stock=5, categoria_id=1)
    except ValueError as err:
        print(f"error esperado {err}")