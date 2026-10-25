bordemos de todo - sistema de gestion de stock y api web

sistema de gestion de inventario y catalogo web para la tienda bordemos de todo. el proyecto integra una aplicacion de escritorio en python para administracion interna y una api rest que expone los datos para un catalogo web en tiempo real.

arquitectura del proyecto

el sistema esta desarrollado bajo una arquitectura en capas (3-tier) utilizando el patron repository:

app de escritorio: desarrollada con pyqt6 para la gestion del inventario local.

backend / api rest: desarrollada con fastapi para servir los datos en formato json.

frontend web: interfaz web construida con html, css y javascript consumiendo la api via fetch.

persistencia: base de datos relacional mysql gestionada con administrador de contexto (context manager) y sql parametrizado.

estructura de carpetas

bordemosdetodo/
├── api/
│   ├── __init__.py
│   └── main_api.py
├── db/
│   ├── __init__.py
│   └── conexion.py
├── frontend/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   └── index.html
├── modelos/
│   ├── __init__.py
│   ├── categoria.py
│   └── parche.py
├── repositorios/
│   ├── __init__.py
│   ├── base_repository.py
│   ├── categoria_repository.py
│   └── parche_repository.py
├── servicios/
│   ├── __init__.py
│   └── parche_service.py
├── sql/
│   └── bordemosdetodo.sql
├── .env.example
├── .gitignore
├── config.py
├── gui.py
├── main.py
├── prueba_conexion.py
├── readme.md
└── requirements.txt


tecnologias utilizadas

python 3.10+

pyqt6

fastapi

uvicorn

mysql

mysql-connector-python

python-dotenv

html5 / css3 / javascript (es6)

requisitos previos

python 3.10 o superior instalado.

servidor mysql en ejecucion.

instalacion y configuracion

clonar el repositorio:
git clone 
cd bordemosdetodo

crear y activar el entorno virtual:
python -m venv .venv
.venv\scripts\activate (windows) o source .venv/bin/activate (linux/mac)

instalar dependencias:
pip install -r requirements.txt

configurar variables de entorno:
crear un archivo .env en la raiz tomando como referencia .env.example:
db_host=localhost
db_port=3306
db_user=tu_usuario
db_password=tu_contraseña
db_name=bordemosdetodo

preparar la base de datos:
ejecutar el script sql/bordemosdetodo.sql en tu cliente mysql.

ejecucion de las aplicaciones

para iniciar la aplicacion de escritorio:
python main.py

para iniciar el servidor de la api web:
uvicorn api.main_api:app --reload

para ver el catalogo web:
abrir el archivo frontend/index.html en un navegador con la api en ejecucion.

endpoints principales de la api

get /api/parches: obtiene la lista completa de parches.

get /api/parches/{id}: obtiene la informacion de un parche especifico.

post /api/parches: registra un nuevo parche en el sistema.