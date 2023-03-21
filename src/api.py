from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.user.views import api_router as user_router
from src.auth.views import api_router as auth_router
from src.admin.views import api_router as admin_router
from src.files.views import api_router as file_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://212.182.25.252:8080",
    "http://powerdrive.skni.umcs.pl",
    "https://powerdrive.skni.umcs.pl",
    "http://smaug.skni.umcs.pl",
    "https://smaug.skni.umcs.pl"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(file_router)


@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}
