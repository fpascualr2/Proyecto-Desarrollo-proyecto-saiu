from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, academico, estudiante, usuario, docente

app = FastAPI(title="SAIU Backend", version="1.0.0")

# Orígenes permitidos para el Frontend (Angular)
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(academico.router)
app.include_router(estudiante.router)  
app.include_router(docente.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Backend de SAIU 🚀"}