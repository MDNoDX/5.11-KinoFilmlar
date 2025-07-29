import os
os.system('cls' if os.name == 'nt' else 'clear')

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routers import film, rating
import uvicorn

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/", tags=['Welcome'])
async def welcome():
    return {"message": "Welcome to the Film Rating API"}

app.include_router(film.router)
app.include_router(rating.router)

if __name__ == "__main__":
    uvicorn.run(app)