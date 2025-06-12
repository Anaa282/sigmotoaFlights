from sqlmodel import Session, select
from typing import List, Optional
from models import User, Pet, Vuelos
from datetime import datetime

# Operaciones de Vuelos
def crear_vuelo(session: Session, origen: str, destino: str, fecha: float, pagado: bool = True) -> Vuelos:

    db_vuelo = Vuelos(origen=origen, destino=destino, fecha=fecha, pagado=pagado)
    session.add(db_vuelo)
    session.commit()
    session.refresh(db_vuelo)
    return db_vuelo

def buscar_vuelos(
    session: Session,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    fecha: Optional[float] = None
) -> List[Vuelos]:

    query = select(Vuelos)
    if origen:
        query = query.where(Vuelos.origen == origen)
    if destino:
        query = query.where(Vuelos.destino == destino)
    if fecha:
        query = query.where(Vuelos.fecha == fecha)
    return session.exec(query).all()

def obtener_vuelo(session: Session, vuelo_id: int) -> Optional[Vuelos]:

    return session.get(Vuelos, vuelo_id)

# Operaciones de Usuario
def crear_usuario(session: Session, nombre: str, reservas: str = "", pet: bool = True) -> User:

    db_usuario = User(nombre=nombre, reservas=reservas, pet=pet)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario

def obtener_usuario(session: Session, user_id: int) -> Optional[User]:

    return session.get(User, user_id)

def reservar_vuelo(session: Session, vuelo_id: int, user_id: int) -> bool:

    usuario = obtener_usuario(session, user_id)
    vuelo = obtener_vuelo(session, vuelo_id)
    
    if not usuario or not vuelo:
        return False
    nuevas_reservas = f"{usuario.reservas},{vuelo_id}" if usuario.reservas else str(vuelo_id)
    usuario.reservas = nuevas_reservas
    session.add(usuario)
    session.commit()
    return True


def crear_mascota(session: Session, nombre: str, size: str, user_id: Optional[int] = None) -> Pet:

    db_mascota = Pet(nombre=nombre, size=size, user_id=user_id)
    session.add(db_mascota)
    session.commit()
    session.refresh(db_mascota)
    return db_mascota

def obtener_mascota(session: Session, id_mascota: int) -> Optional[Pet]:
    return session.get(Pet, id_mascota)

def asignar_mascota_usuario(session: Session, user_id: int, id_mascota: int) -> bool:
    usuario = obtener_usuario(session, user_id)
    mascota = obtener_mascota(session, id_mascota)
    
    if not usuario or not mascota:
        return False
    
    usuario.pet = True
    usuario.pet_id = id_mascota
    mascota.user_id = user_id
    session.add(usuario)
    session.add(mascota)
    session.commit()
    return True