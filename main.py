from fastapi import FastAPI
from database import create_db
from routers.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(router)