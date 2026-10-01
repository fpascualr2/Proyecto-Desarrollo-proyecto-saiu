from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import get_password_hash

db = SessionLocal()

def crear_usuario_prueba():
    usuario_existente = db.query(Usuario).filter(Usuario.username == "admin").first()
    if not usuario_existente:
        nuevo_usuario = Usuario(
            username="admin",
            email="admin@sistema.com",
            nombre="Administrador",
            apellido="Prueba",
            password_hash=get_password_hash("admin123"),
            rol="admin"
        )
        db.add(nuevo_usuario)
        db.commit()
        print("Usuario de prueba creado. Username: admin | Password: admin123")
    else:
        print("El usuario de prueba ya existe en la base de datos.")

if __name__ == "__main__":
    crear_usuario_prueba()
    db.close()