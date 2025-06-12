from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List
from connection_db import get_session
from models import User, Pet, Vuelos, VueloSearch, VueloReserva
import operations

app = FastAPI(
)


@app.post("/vuelos/", response_model=Vuelos, tags=["Vuelos"])
def crear_vuelo(
    origen: str,
    destino: str,
    fecha: float,
    pagado: bool = True,
    session: Session = Depends(get_session)
):

    return operations.crear_vuelo(session, origen, destino, fecha, pagado)

@app.post("/vuelos/buscar/", response_model=List[Vuelos], tags=["Vuelos"])
def buscar_vuelos(
    busqueda: VueloSearch,
    session: Session = Depends(get_session)
):

    return operations.buscar_vuelos(
        session,
        origen=busqueda.origen,
        destino=busqueda.destino,
        fecha=busqueda.fecha
    )


@app.post("/usuarios/", response_model=User, tags=["Usuarios"])
def crear_usuario(
    nombre: str,
    reservas: str = "",
    pet: bool = True,
    session: Session = Depends(get_session)
):

    try:
        return operations.crear_usuario(session, nombre, reservas, pet)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reservas/", tags=["Reservas"])
def crear_reserva(
    reserva: VueloReserva,
    session: Session = Depends(get_session)
):

    if operations.reservar_vuelo(session, reserva.vuelo_id, reserva.user_id):
        return {"mensaje": "Reserva creada exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario o vuelo no encontrado")


@app.post("/mascotas/", response_model=Pet, tags=["Mascotas"])
def crear_mascota(
    nombre: str,
    size: str,
    user_id: int = None,
    session: Session = Depends(get_session)
):

    return operations.crear_mascota(session, nombre, size, user_id)

@app.post("/usuarios/{user_id}/mascotas/{id_mascota}", tags=["Usuarios", "Mascotas"])
def asignar_mascota(
    user_id: int,
    id_mascota: int,
    session: Session = Depends(get_session)
):

    if operations.asignar_mascota_usuario(session, user_id, id_mascota):
        return {"mensaje": "Mascota asignada exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario o mascota no encontrado")

# Endpoints de consulta
@app.get("/usuarios/{user_id}", response_model=User, tags=["Usuarios"])
def obtener_usuario(
    user_id: int,
    session: Session = Depends(get_session)
):

    usuario = operations.obtener_usuario(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/mascotas/{id_mascota}", response_model=Pet, tags=["Mascotas"])
def obtener_mascota(
    id_mascota: int,
    session: Session = Depends(get_session)
):

    mascota = operations.obtener_mascota(session, id_mascota)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota