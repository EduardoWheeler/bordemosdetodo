import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class ConfigDB:
    host: str = os.getenv("DB_HOST", os.getenv("db_host", "localhost"))
    port: int = int(os.getenv("DB_PORT", os.getenv("db_port", "3306")))
    user: str = os.getenv("DB_USER", os.getenv("db_user", ""))
    password: str = os.getenv("DB_PASSWORD", os.getenv("db_password", ""))
    database: str = os.getenv("DB_NAME", os.getenv("db_name", ""))
