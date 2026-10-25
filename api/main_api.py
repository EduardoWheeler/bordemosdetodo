from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

# Importamos las capas existentes de tu proyecto de escritorio
from repositorios.parche_repository import ParcheRepository
from modelos.parche import Parche

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Bordemos de Todo - API Oficial",
    description="API RESTful para conectar la base de datos de parches con la app de escritorio y la web.",
    version="1.0.0"
)

# Configuración de CORS (Permite que cualquier página web o app externa consuma esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes restringir esto a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia del repositorio
repo_parche = ParcheRepository()

# --- ESQUEMAS PYDANTIC (Validación de datos de entrada/salida para la web) ---
class ParcheResponse(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    precio: int
    stock: int
    categoria_id: int
    es_personalizado: bool

    class Config:
        from_attributes = True

class ParcheCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    precio: int = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    categoria_id: int
    es_personalizado: bool = False


# --- ENDPOINTS DE LA API ---

@app.get("/", tags=["General"])
def inicio():
    """Ruta raíz para comprobar que la API está funcionando."""
    return {"mensaje": "Bienvenido a la API de Bordemos de Todo 🪡✨"}


@app.get("/api/parches", response_model=List[ParcheResponse], tags=["Parches"])
def listar_parches():
    """Devuelve la lista completa de parches registrados en la base de datos."""
    try:
        parches = repo_parche.listar()
        # Convertimos los objetos Parche a diccionarios o modelos compatibles
        resultado = []
        for p in parches:
            resultado.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "precio": p.precio,
                "stock": p.stock,
                "categoria_id": p.categoria_id,
                "es_personalizado": p.es_personalizado
            })
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los parches: {str(e)}"
        )


@app.get("/api/parches/{parche_id}", response_model=ParcheResponse, tags=["Parches"])
def obtener_parche(parche_id: int):
    """Busca un parche específico por su ID."""
    try:
        p = repo_parche.buscar_por_id(parche_id)
        if not p:
            raise HTTPException(status_code=404, detail="Parche no encontrado")
        return {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "stock": p.stock,
            "categoria_id": p.categoria_id,
            "es_personalizado": p.es_personalizado
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el servidor: {str(e)}"
        )


@app.post("/api/parches", status_code=status.HTTP_201_CREATED, tags=["Parches"])
def crear_parche(parche_data: ParcheCreate):
    """Permite registrar un nuevo parche (ideal para formularios web o app de escritorio)."""
    try:
        nuevo_parche = Parche(
            nombre=parche_data.nombre,
            descripcion=parche_data.descripcion,
            precio=parche_data.precio,
            stock=parche_data.stock,
            categoria_id=parche_data.categoria_id,
            es_personalizado=parche_data.es_personalizado
        )
        nuevo_id = repo_parche.insertar(nuevo_parche)
        return {"mensaje": "Parche creado exitosamente", "id": nuevo_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo guardar el parche: {str(e)}"
        )