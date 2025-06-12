from typing import Optional
from sqlmodel import SQLModel, Field

class Vuelos (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: str = Field(index=True, unique=True)
    destino: str
    fecha: float
    pagado: bool

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    reservas: str
    mascota:bool

class Mascotas(SQLModel, table=True):
    id_usuario: int=Field(default=None, primary_key=True)
    id_Mascotas: int=Field(default=None, primary_key=True)
    nombre: str= Field(default=None, primary_key=True)
    size: str

