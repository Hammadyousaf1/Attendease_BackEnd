from fastapi import FastAPI
from app.routes import train, recognize

app = FastAPI()

app.include_router(train.router)
app.include_router(recognize.router)

@app.get("/")
def read_root():
    return {"message": "Face Recognition Backend"}