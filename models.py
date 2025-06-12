from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Vuelos(SQLModel, table=True):
    __tablename__ = "Vuelos"
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: str = Field(index=True)
    destino: str
    fecha: str
    pagado: bool = Field(default=False)


class User(SQLModel, table=True):
    __tablename__ = "Usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    reservas: str = Field(default="")
    pet: bool = Field(default=True)
    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id_mascotas")


class Pet(SQLModel, table=True):
    id_mascotas: int = Field(default=None, primary_key=True)
    nombre: str
    size: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class VueloSearch(BaseModel):
    origen: Optional[str] = None
    destino: Optional[str] = None
    fecha: Optional[str] = None


class VueloReserva(BaseModel):
    vuelo_id: int
    user_id: int