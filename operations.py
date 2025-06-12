from sqlmodel import Session
from models import User, Pet, Vuelos, VueloSearch
from typing import List

def crear_vuelo(session: Session, origen: str, destino: str, fecha: str, pagado: bool = False) -> Vuelos:
    vuelo = Vuelos(origen=origen, destino=destino, fecha=fecha, pagado=False)
    session.add(vuelo)
    session.commit()
    session.refresh(vuelo)
    return vuelo

def buscar_vuelos(session: Session, origen: str, destino: str, fecha: str) -> List[Vuelos]:
    vuelos = session.query(Vuelos).filter(
        Vuelos.origen == origen,
        Vuelos.destino == destino,
        Vuelos.fecha == fecha
    ).all()
    return vuelos

def crear_usuario(session: Session, nombre: str, reservas: str, pet: bool) -> User:
    usuario = User(nombre=nombre, reservas=reservas, pet=pet)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def reservar_vuelo(session: Session, vuelo_id: int, user_id: int) -> bool:
    usuario = session.query(User).filter(User.id == user_id).first()
    vuelo = session.query(Vuelos).filter(Vuelos.id == vuelo_id).first()
    
    if usuario and vuelo:
        if usuario.reservas:
            usuario.reservas = f"{usuario.reservas},{vuelo_id}"
        else:
            usuario.reservas = str(vuelo_id)
        
        vuelo.pagado = True
        session.commit()
        return True
    return False

def crear_mascota(session: Session, nombre: str, size: str, user_id: int = None) -> Pet:
    mascota = Pet(nombre=nombre, size=size, user_id=user_id)
    session.add(mascota)
    session.commit()
    session.refresh(mascota)
    return mascota

def asignar_mascota_usuario(session: Session, user_id: int, id_mascota: int) -> bool:
    usuario = session.query(User).filter(User.id == user_id).first()
    mascota = session.query(Pet).filter(Pet.id == id_mascota).first()
    
    if usuario and mascota:
        mascota.user_id = user_id
        session.commit()
        return True
    return False

def obtener_usuario(session: Session, user_id: int) -> User:
    return session.query(User).filter(User.id == user_id).first()

def obtener_mascota(session: Session, id_mascota: int) -> Pet:
    return session.query(Pet).filter(Pet.id == id_mascota).first()

def borrar_usuario(session: Session, user_id: int) -> bool:
    usuario = session.query(User).filter(User.id == user_id).first()
    if usuario:
        session.delete(usuario)
        session.commit()
        return True
    return False

def borrar_mascota(session: Session, id_mascota: int) -> bool:
    mascota = session.query(Pet).filter(Pet.id == id_mascota).first()
    if mascota:
        session.delete(mascota)
        session.commit()
        return True
    return False