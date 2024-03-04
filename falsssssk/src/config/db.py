from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from src.config.config import DATABASE_URI
from sqlalchemy import create_engine
from src.config.base import Base

engine = create_engine(DATABASE_URI)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos.")
    except OperationalError as e:
        print("Error al conectar con la base de datos:", e)

