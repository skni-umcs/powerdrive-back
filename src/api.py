from fastapi import FastAPI
from src.user.views import api_router as user_router
from src.auth.views import api_router as auth_router
from src.admin.views import api_router as admin_router
app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    """Health check"""
    return {"status": "ok"}
