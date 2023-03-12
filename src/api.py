from fastapi import FastAPI
from src.user.views import api_router as user_router
from src.files.views import api_router as file_router

app = FastAPI()
app.include_router(user_router)
app.include_router(file_router)


@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}
