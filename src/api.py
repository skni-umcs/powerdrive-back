from fastapi import FastAPI
from src.user.views import api_router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}
