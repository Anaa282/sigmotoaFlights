from typing import Optional
from sqlmodel import SQLModel, Field

class Vuelos (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: str = Field(index=True, unique=True)
    disponible: bool = Field(default=True)
    destino: str
    fecha: float
    pagado: bool = Field(default=True)

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    reservas: str
    mascota:bool = Field(default=True)

class Mascotas(SQLModel, table=True):
    id_usuario: int=Field(default=None, primary_key=True)
    id_Mascotas: int=Field(default=None, primary_key=True)
    nombre: str= Field(default=None, primary_key=True)
    size: str

