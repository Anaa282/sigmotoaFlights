import os
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()


DEFAULT_DB_URL = "sqlite:///data.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)


engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def create_db_and_tables():
    try:
        print("Intentando conectar a la base de datos y crear/verificar tablas...")
        SQLModel.metadata.create_all(engine)
        print("Tablas de la base de datos creadas/verificadas exitosamente.")
    except Exception as e:
        print(f"ERROR al crear/verificar tablas de la base de datos: {e}")

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session