from sqlmodel import create_engine, Session
from sqlmodel import SQLModel

DATABASE_URL = "postgresql://parcial_finalds_user:2yseqW7n6c72tnPOQKqImoljnDfBt0Nw@dpg-d15g19vdiees7380pgag-a.oregon-postgres.render.com/parcial_finalds"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    engine = create_engine(DATABASE_URL)

    try:
        print("Creando tablas si no existen...")
        SQLModel.metadata.create_all(engine)
        print("¡Proceso de verificación/creación de tablas completado exitosamente!")
        return engine

    except Exception as e:
        print(f"Error durante la actualización de la base de datos: {e}")
        raise

if __name__ == "__main__":
    print("Iniciando verificación de la base de datos...")
    init_db()
    print("¡Proceso completado!")