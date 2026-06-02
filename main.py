from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.router import text_ingesation
from src.service.moderation_service import load_model
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(text_ingesation.router)

@app.get("/main")
def pong():
    return {"ping": "pong!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
