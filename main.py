from fastapi import FastAPI
from src.router import text_ingesation
import uvicorn

app = FastAPI()
app.include_router(text_ingesation.router)

@app.get("/main")
def pong():
    return {"ping": "pong!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)