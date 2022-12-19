# from src.api import app
import uvicorn


if __name__ == "__main__":
    uvicorn.run("src.api:app", port=8123, host="0.0.0.0", reload=True, )

