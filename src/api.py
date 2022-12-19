from fastapi import FastAPI
from src.user.views import api_router as user_router
from src.group.views import api_router as group_router

app = FastAPI()
app.include_router(user_router)
app.include_router(group_router)
@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}
