from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# Asegurar que el directorio raíz esté en el path para importar repositorios y modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositorios.parche_repositorio import ParcheRepositorio

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Bordemos de Todo API",
    description="API REST para la gestión de inventario y catálogo online de Bordemos de Todo.",
    version="1.1.0"
)

# Configurar CORS para permitir peticiones desde cualquier origen web o app de escritorio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar el repositorio de la base de datos
repo_parche = ParcheRepositorio()

# ==========================================
# MODELOS PYDANTIC (Esquemas de Datos)
# ==========================================
class ParcheResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    es_personalizado: bool

    class Config:
        from_attributes = True

class ItemPedido(BaseModel):
    parche_id: int
    cantidad: int = Field(gt=0, description="La cantidad debe ser mayor a 0")

class PedidoCreate(BaseModel):
    nombre_cliente: str = Field(min_length=2, description="Nombre del comprador")
    email_cliente: str = Field(description="Email de contacto")
    items: List[ItemPedido] = Field(min_items=1, description="El pedido debe tener al menos un parche")

class PedidoResponse(BaseModel):
    mensaje: str
    total_compra: float
    items_procesados: int

# ==========================================
# ENDPOINTS / RUTAS DE LA API
# ==========================================
@app.get("/", tags=["Estado del Sistema"])
def raiz():
    """Endpoint raíz para verificar que el servidor FastAPI está operativo."""
    return {
        "mensaje": "Bienvenido a la API REST de Bordemos de Todo",
        "estado": "activo",
        "documentacion": "/docs"
    }

@app.get("/api/parches", response_model=List[ParcheResponse], tags=["Catálogo"])
def obtener_todos_los_parches():
    """
    Retorna la lista completa de parches disponibles en la base de datos MySQL.
    """
    try:
        # Llamamos a listar() que es el método estándar definido en ParcheRepositorio
        parches = repo_parche.listar()
        return parches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los parches desde la base de datos: {str(e)}"
        )

@app.post("/api/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def procesar_pedido(pedido: PedidoCreate):
    """
    Procesa la compra de parches desde la tienda web.
    Valida el stock disponible y descuenta automáticamente las unidades vendidas en MySQL.
    """
    total_compra = 0.0
    items_procesados = 0
    try:
        # 1. Validar existencia y stock de cada ítem
        for item in pedido.items:
            parche = repo_parche.buscar_por_id(item.parche_id)
            if not parche:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El parche con ID {item.parche_id} no existe en el catálogo."
                )
            if parche.stock < item.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para '{parche.nombre}'. Disponible: {parche.stock}, Solicitado: {item.cantidad}."
                )

        # 2. Procesar cálculos y actualizar stock
        for item in pedido.items:
            parche = repo_parche.buscar_por_id(item.parche_id)
            nuevo_stock = parche.stock - item.cantidad
            total_compra += float(parche.precio) * item.cantidad
            items_procesados += item.cantidad
            
            # Actualizamos stock utilizando el método de actualización del repositorio
            parche.stock = nuevo_stock
            repo_parche.actualizar(parche)

        return {
            "mensaje": f"¡Pedido registrado con éxito para {pedido.nombre_cliente}!",
            "total_compra": round(total_compra, 2),
            "items_procesados": items_procesados
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el pedido: {str(e)}"
        )