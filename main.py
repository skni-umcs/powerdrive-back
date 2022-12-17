# from src.api import app
import uvicorn
from src.config import Settings

sett = Settings()

if __name__ == "__main__":
    uvicorn.run("src.api:app", port=sett.app_port, host="0.0.0.0", reload=True, )
