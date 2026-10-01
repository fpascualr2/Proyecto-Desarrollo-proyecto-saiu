from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, academico, estudiante

app = FastAPI(title="SAIU Backend", version="1.0.0")

# Configuración de CORS para que Angular pueda comunicarse sin problemas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(academico.router)
app.include_router(estudiante.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Backend de SAIU - Sistema Académico Universitario"}