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
    fecha: str,

    session: Session = Depends(get_session)
):
    try:
        return operations.crear_vuelo(session, origen, destino, fecha)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear vuelo: {str(e)}")

@app.post("/vuelos/buscar/", response_model=List[Vuelos], tags=["Vuelos"])
def buscar_vuelos(
    busqueda: VueloSearch,
    session: Session = Depends(get_session)
):
    try:
        vuelos = operations.buscar_vuelos(
            session,
            origen=busqueda.origen,
            destino=busqueda.destino,
            fecha=busqueda.fecha
        )
        if not vuelos:
            raise HTTPException(status_code=404, detail="No se encontraron vuelos con los criterios especificados")
        return vuelos
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la búsqueda: {str(e)}")

@app.post("/usuarios/", response_model=User, tags=["Usuarios"])
def crear_usuario(
    nombre: str,
    reservas: str = "",
    pet: bool = True,
    session: Session = Depends(get_session)
):
    try:
        return operations.crear_usuario(session, nombre, reservas, pet)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

@app.post("/reservas/", tags=["Reservas"])
def crear_reserva(
    reserva: VueloReserva,
    session: Session = Depends(get_session)
):
    try:
        if operations.reservar_vuelo(session, reserva.vuelo_id, reserva.user_id):
            return {"mensaje": "Reserva creada exitosamente"}
        raise HTTPException(status_code=404, detail="Usuario o vuelo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear reserva: {str(e)}")

@app.post("/mascotas/", response_model=Pet, tags=["Mascotas"])
def crear_mascota(
    nombre: str,
    size: str,
    user_id: int = None,
    session: Session = Depends(get_session)
):
    try:
        return operations.crear_mascota(session, nombre, size, user_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear mascota: {str(e)}")

@app.post("/usuarios/{user_id}/mascotas/{id_mascota}", tags=["Usuarios", "Mascotas"])
def asignar_mascota(
    user_id: int,
    id_mascota: int,
    session: Session = Depends(get_session)
):
    try:
        if operations.asignar_mascota_usuario(session, user_id, id_mascota):
            return {"mensaje": "Mascota asignada exitosamente"}
        raise HTTPException(status_code=404, detail="Usuario o mascota no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al asignar mascota: {str(e)}")

@app.get("/usuarios/{user_id}", response_model=User, tags=["Usuarios"])
def obtener_usuario(
    user_id: int,
    session: Session = Depends(get_session)
):
    try:
        usuario = operations.obtener_usuario(session, user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener usuario: {str(e)}")

@app.get("/mascotas/{id_mascota}", response_model=Pet, tags=["Mascotas"])
def obtener_mascota(
    id_mascota: int,
    session: Session = Depends(get_session)
):
    try:
        mascota = operations.obtener_mascota(session, id_mascota)
        if not mascota:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return mascota
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener mascota: {str(e)}")

@app.delete("/usuarios/{user_id}", tags=["Usuarios"])
def borrar_usuario(
    user_id: int,
    session: Session = Depends(get_session)
):
    try:
        if operations.borrar_usuario(session, user_id):
            return {"mensaje": "Usuario eliminado exitosamente"}
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/mascotas/{id_mascota}", tags=["Mascotas"])
def borrar_mascota(
    id_mascota: int,
    session: Session = Depends(get_session)
):
    try:
        if operations.borrar_mascota(session, id_mascota):
            return {"mensaje": "Mascota eliminada exitosamente"}
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))