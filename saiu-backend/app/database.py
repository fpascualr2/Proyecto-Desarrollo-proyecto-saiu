import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Toma la URL de la base de datos desde el archivo .env
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "mysql+pymysql://root:12345@localhost:3306/saiu_db")

# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()