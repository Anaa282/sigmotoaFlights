from typing import List, Optional
from sqlmodel import Session, select
from models import User, Pet, Vuelos


# Operaciones de Usuario
def create_user(
    session: Session,
    nombre: str,
    reservas: str = "",
    pet: bool = True,
    pet_id: Optional[int] = None
) -> User:
    db_user = User(nombre=nombre, reservas=reservas, pet=pet, pet_id=pet_id)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_name(session: Session, nombre: str) -> Optional[User]:
    statement = select(User).where(User.nombre == nombre)
    return session.exec(statement).first()


def get_all_users(session: Session) -> List[User]:
    statement = select(User)
    return session.exec(statement).all()


def update_user(
    session: Session,
    user_id: int,
    nombre: Optional[str] = None,
    reservas: Optional[str] = None,
    pet: Optional[bool] = None,
    pet_id: Optional[int] = None
) -> Optional[User]:
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    
    user_data = {}
    if nombre is not None:
        user_data["nombre"] = nombre
    if reservas is not None:
        user_data["reservas"] = reservas
    if pet is not None:
        user_data["pet"] = pet
    if pet_id is not None:
        user_data["pet_id"] = pet_id

    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> bool:
    db_user = session.get(User, user_id)
    if not db_user:
        return False
    session.delete(db_user)
    session.commit()
    return True



def create_pet(
    session: Session,
    nombre: str,
    size: str,
    user_id: Optional[int] = None
) -> Pet:
    db_pet = Pet(nombre=nombre, size=size, user_id=user_id)
    session.add(db_pet)
    session.commit()
    session.refresh(db_pet)
    return db_pet


def get_pet(session: Session, id_mascotas: int, nombre: str) -> Optional[Pet]:
    statement = select(Pet).where(Pet.id_mascotas == id_mascotas, Pet.nombre == nombre)
    return session.exec(statement).first()


def get_all_pets(session: Session) -> List[Pet]:
    statement = select(Pet)
    return session.exec(statement).all()


def get_user_pets(session: Session, user_id: int) -> List[Pet]:
    statement = select(Pet).where(Pet.user_id == user_id)
    return session.exec(statement).all()


def update_pet(
    session: Session,
    id_mascotas: int,
    nombre: str,
    new_nombre: Optional[str] = None,
    size: Optional[str] = None,
    user_id: Optional[int] = None
) -> Optional[Pet]:
    db_pet = session.exec(
        select(Pet).where(Pet.id_mascotas == id_mascotas, Pet.nombre == nombre)
    ).first()
    
    if not db_pet:
        return None

    if new_nombre is not None:
        db_pet.nombre = new_nombre
    if size is not None:
        db_pet.size = size
    if user_id is not None:
        db_pet.user_id = user_id

    session.add(db_pet)
    session.commit()
    session.refresh(db_pet)
    return db_pet


def delete_pet(session: Session, id_mascotas: int, nombre: str) -> bool:
    db_pet = session.exec(
        select(Pet).where(Pet.id_mascotas == id_mascotas, Pet.nombre == nombre)
    ).first()
    
    if not db_pet:
        return False
    
    session.delete(db_pet)
    session.commit()
    return True



def assign_pet_to_user(
    session: Session,
    user_id: int,
    pet_id: int,
    pet_nombre: str
) -> bool:
    db_user = session.get(User, user_id)
    db_pet = session.exec(
        select(Pet).where(Pet.id_mascotas == pet_id, Pet.nombre == pet_nombre)
    ).first()

    if not db_user or not db_pet:
        return False

    db_user.pet_id = pet_id
    db_pet.user_id = user_id
    
    session.add(db_user)
    session.add(db_pet)
    session.commit()
    return True


def unassign_pet_from_user(session: Session, user_id: int) -> bool:
    db_user = session.get(User, user_id)
    if not db_user:
        return False

    if db_user.pet_id:
        db_pet = session.get(Pet, db_user.pet_id)
        if db_pet:
            db_pet.user_id = None
            session.add(db_pet)
    
    db_user.pet_id = None
    session.add(db_user)
    session.commit()
    return True



def create_vuelo(
    session: Session,
    origen: str,
    destino: str,
    fecha: float,
    pagado: bool = True
) -> Vuelos:
    db_vuelo = Vuelos(origen=origen, destino=destino, fecha=fecha, pagado=pagado)
    session.add(db_vuelo)
    session.commit()
    session.refresh(db_vuelo)
    return db_vuelo


def get_vuelo(session: Session, vuelo_id: int) -> Optional[Vuelos]:
    return session.get(Vuelos, vuelo_id)


def search_vuelos(
    session: Session,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    fecha: Optional[float] = None
) -> List[Vuelos]:
    statement = select(Vuelos)
    if origen:
        statement = statement.where(Vuelos.origen == origen)
    if destino:
        statement = statement.where(Vuelos.destino == destino)
    if fecha:
        statement = statement.where(Vuelos.fecha == fecha)
    return session.exec(statement).all()


def update_vuelo(
    session: Session,
    vuelo_id: int,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    fecha: Optional[float] = None,
    pagado: Optional[bool] = None
) -> Optional[Vuelos]:
    db_vuelo = session.get(Vuelos, vuelo_id)
    if not db_vuelo:
        return None

    if origen is not None:
        db_vuelo.origen = origen
    if destino is not None:
        db_vuelo.destino = destino
    if fecha is not None:
        db_vuelo.fecha = fecha
    if pagado is not None:
        db_vuelo.pagado = pagado

    session.add(db_vuelo)
    session.commit()
    session.refresh(db_vuelo)
    return db_vuelo


def delete_vuelo(session: Session, vuelo_id: int) -> bool:
    db_vuelo = session.get(Vuelos, vuelo_id)
    if not db_vuelo:
        return False
    session.delete(db_vuelo)
    session.commit()
    return True