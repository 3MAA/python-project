from fastapi import FastAPI
from app.api import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Math Microservice API",
    description="API for math operations: pow, fibonacci, factorial",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

app.include_router(router)
