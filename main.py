from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List, Optional
from connection_db import get_session
from models import User, Pet, Vuelos, VueloSearch, VueloReserva
from operations import (
    create_user, get_user, get_user_by_name, get_all_users, update_user, delete_user,
    create_pet, get_pet, get_all_pets, get_user_pets, update_pet, delete_pet,
    assign_pet_to_user, unassign_pet_from_user,
    create_vuelo, get_vuelo, search_vuelos, update_vuelo, delete_vuelo
)
from pydantic import BaseModel

app = FastAPI()

# Modelos Pydantic para las peticiones
class UserCreate(BaseModel):
    nombre: str
    reservas: str = ""
    pet: bool = True
    pet_id: Optional[int] = None

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    reservas: Optional[str] = None
    pet: Optional[bool] = None
    pet_id: Optional[int] = None

class PetCreate(BaseModel):
    nombre: str
    size: str
    user_id: Optional[int] = None

class PetUpdate(BaseModel):
    new_nombre: Optional[str] = None
    size: Optional[str] = None
    user_id: Optional[int] = None

class VueloCreate(BaseModel):
    origen: str
    destino: str
    fecha: float
    pagado: bool = True

# Endpoints para Vuelos
@app.post("/vuelos/", response_model=Vuelos)
def create_new_vuelo(
    vuelo: VueloCreate,
    session: Session = Depends(get_session)
):
    return create_vuelo(
        session=session,
        origen=vuelo.origen,
        destino=vuelo.destino,
        fecha=vuelo.fecha,
        pagado=vuelo.pagado
    )

@app.get("/vuelos/search", response_model=List[Vuelos])
def search_vuelos_endpoint(
    search_params: VueloSearch,
    session: Session = Depends(get_session)
):
    return search_vuelos(
        session=session,
        origen=search_params.origen,
        destino=search_params.destino,
        fecha=search_params.fecha
    )

@app.get("/vuelos/{vuelo_id}", response_model=Vuelos)
def get_vuelo_by_id(
    vuelo_id: int,
    session: Session = Depends(get_session)
):
    db_vuelo = get_vuelo(session, vuelo_id)
    if not db_vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return db_vuelo

# Endpoints para Usuarios
@app.post("/users/", response_model=User)
def create_new_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = get_user_by_name(session, user.nombre)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado"
        )
    return create_user(
        session=session,
        nombre=user.nombre,
        reservas=user.reservas,
        pet=user.pet,
        pet_id=user.pet_id
    )

@app.get("/users/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    users = get_all_users(session)
    return users[skip : skip + limit]

@app.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    db_user = get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.get("/users/name/{nombre}", response_model=User)
def read_user_by_name(
    nombre: str,
    session: Session = Depends(get_session)
):
    db_user = get_user_by_name(session, nombre)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.put("/users/{user_id}", response_model=User)
def update_user_info(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session)
):
    updated_user = update_user(
        session=session,
        user_id=user_id,
        nombre=user.nombre,
        reservas=user.reservas,
        pet=user.pet,
        pet_id=user.pet_id
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user_by_id(
    user_id: int,
    session: Session = Depends(get_session)
):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

# Endpoints para Mascotas
@app.post("/pets/", response_model=Pet)
def create_new_pet(
    pet: PetCreate,
    session: Session = Depends(get_session)
):
    return create_pet(
        session=session,
        nombre=pet.nombre,
        size=pet.size,
        user_id=pet.user_id
    )

@app.get("/pets/", response_model=List[Pet])
def read_pets(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    pets = get_all_pets(session)
    return pets[skip : skip + limit]

@app.get("/pets/{id_mascotas}/{nombre}", response_model=Pet)
def read_pet(
    id_mascotas: int,
    nombre: str,
    session: Session = Depends(get_session)
):
    db_pet = get_pet(session, id_mascotas, nombre)
    if not db_pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return db_pet

@app.get("/users/{user_id}/pets", response_model=List[Pet])
def read_user_pets_list(
    user_id: int,
    session: Session = Depends(get_session)
):
    pets = get_user_pets(session, user_id)
    return pets

@app.put("/pets/{id_mascotas}/{nombre}", response_model=Pet)
def update_pet_info(
    id_mascotas: int,
    nombre: str,
    pet: PetUpdate,
    session: Session = Depends(get_session)
):
    updated_pet = update_pet(
        session=session,
        id_mascotas=id_mascotas,
        nombre=nombre,
        new_nombre=pet.new_nombre,
        size=pet.size,
        user_id=pet.user_id
    )
    if not updated_pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return updated_pet

@app.delete("/pets/{id_mascotas}/{nombre}")
def delete_pet_by_id(
    id_mascotas: int,
    nombre: str,
    session: Session = Depends(get_session)
):
    success = delete_pet(session, id_mascotas, nombre)
    if not success:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"message": "Mascota eliminada exitosamente"}

# Endpoints para gestionar relaciones Usuario-Mascota
@app.post("/users/{user_id}/pets/{pet_id}/{pet_nombre}")
def assign_pet_to_user_endpoint(
    user_id: int,
    pet_id: int,
    pet_nombre: str,
    session: Session = Depends(get_session)
):
    success = assign_pet_to_user(session, user_id, pet_id, pet_nombre)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No se pudo asignar la mascota al usuario"
        )
    return {"message": "Mascota asignada exitosamente"}

@app.delete("/users/{user_id}/pet")
def unassign_pet_from_user_endpoint(
    user_id: int,
    session: Session = Depends(get_session)
):
    success = unassign_pet_from_user(session, user_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No se pudo desasignar la mascota del usuario"
        )
    return {"message": "Mascota desasignada exitosamente"}